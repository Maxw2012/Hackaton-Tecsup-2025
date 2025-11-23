from django.http import HttpResponse, JsonResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from web_project import TemplateLayout
import json
import os

from .models import ChatMessage
from .gemini_client import GeminiClient
from apps.prediction.models import DropoutPrediction, StudentCharacteristics


class ChatView(TemplateView):
    """
    Vista principal del chatbot usando el layout de Materio.
    """
    template_name = "chatbot_chat.html"
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


def get_prediction_context(user):
    """
    Obtiene el contexto de la prediccion de desercion del usuario autenticado.
    """
    if not user or not user.is_authenticated or user.is_staff:
        return None
    
    try:
        prediction = DropoutPrediction.objects.filter(user=user).order_by('-created_at').first()
        if not prediction:
            return None
        
        try:
            characteristics = StudentCharacteristics.objects.get(user=user)
        except StudentCharacteristics.DoesNotExist:
            characteristics = None
        
        context_parts = []
        context_parts.append(f"Riesgo de Desercion: {prediction.risk_percentage:.2f}% ({prediction.risk_level})")
        context_parts.append(f"Prediccion: {prediction.prediction_label}")
        
        if characteristics and characteristics.course:
            context_parts.append(f"Curso: {characteristics.course.nombre} (Codigo: {characteristics.course.codigo})")
        
        if characteristics:
            context_parts.append(f"Edad al momento de inscripcion: {characteristics.age_at_enrollment} anos")
            if characteristics.scholarship_holder:
                context_parts.append("Tiene beca")
            if characteristics.debtor:
                context_parts.append("Tiene deudas pendientes")
            if not characteristics.tuition_fees_up_to_date:
                context_parts.append("Matricula no esta al dia")
        
        return "\n".join(context_parts)
        
    except Exception:
        return None


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """
    API endpoint para enviar mensajes al chatbot desde la web.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'El mensaje no puede estar vacio'
            })
        
        if not os.getenv('GEMINI_API_KEY'):
            return JsonResponse({
                'success': False,
                'error': 'API key de Gemini no configurada'
            })
        
        prediction_context = None
        if request.user.is_authenticated:
            prediction_context = get_prediction_context(request.user)
        
        try:
            gemini_client = GeminiClient()
            bot_response = gemini_client.chat(user_message, prediction_context=prediction_context)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al conectar con Gemini: {str(e)}'
            })
        
        chat_message = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_message=user_message,
            bot_response=bot_response,
            model_used=GeminiClient.MODEL
        )
        
        return JsonResponse({
            'success': True,
            'response': bot_response,
            'message_id': chat_message.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON invalido'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })


class ChatHistoryView(TemplateView):
    """
    Vista para mostrar el historial de conversaciones usando el layout de Materio.
    """
    template_name = "chatbot_history.html"
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        messages = ChatMessage.objects.all()[:50]  # ultimos 50 mensajes
        context['messages'] = messages
        return context


@csrf_exempt
@require_http_methods(["POST"])
def twilio_whatsapp_webhook(request):
    """
    Webhook de Twilio WhatsApp Sandbox: recibe mensajes entrantes,
    usa ALMA/Gemini para responder y devuelve TwiML.
    """
    incoming_body = request.POST.get("Body", "").strip()
    from_number = request.POST.get("From") or request.POST.get("WaId")

    if not incoming_body:
        twiml = '<?xml version="1.0" encoding="UTF-8"?><Response><Message>Necesito un mensaje de texto para ayudarte.</Message></Response>'
        return HttpResponse(twiml, content_type="text/xml")

    prediction_context = None
    if getattr(request, "user", None) and request.user.is_authenticated:
        prediction_context = get_prediction_context(request.user)

    if not os.getenv("GEMINI_API_KEY"):
        twiml = '<?xml version="1.0" encoding="UTF-8"?><Response><Message>Configura GEMINI_API_KEY en el servidor.</Message></Response>'
        return HttpResponse(twiml, content_type="text/xml")

    try:
        bot_response = GeminiClient().chat(
            incoming_body,
            prediction_context=prediction_context,
        )

        ChatMessage.objects.create(
            user=None,
            user_message=f"{from_number or 'whatsapp'}: {incoming_body}",
            bot_response=bot_response,
            model_used=GeminiClient.MODEL,
        )
    except Exception:
        bot_response = "Tuvimos un problema al responder. Intenta de nuevo en unos minutos."

    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{escape(bot_response)}</Message></Response>'
    return HttpResponse(twiml, content_type="text/xml")


@csrf_exempt
@require_http_methods(["GET"])
def twilio_status_callback(request):
    """
    Endpoint opcional para recibir los estados de entrega desde Twilio.
    """
    status_data = {
        "MessageSid": request.GET.get("MessageSid"),
        "MessageStatus": request.GET.get("MessageStatus"),
        "From": request.GET.get("From"),
        "To": request.GET.get("To"),
        "ErrorCode": request.GET.get("ErrorCode"),
    }
    return JsonResponse({"success": True, "status": status_data})
