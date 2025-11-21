from django.shortcuts import render
from django.http import JsonResponse
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
    Vista principal del chatbot usando el layout de Materio
    """
    template_name = "chatbot_chat.html"
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

def get_prediction_context(user):
    """
    Obtiene el contexto de la predicción de deserción del usuario
    """
    if not user or not user.is_authenticated or user.is_staff:
        return None
    
    try:
        # Obtener la predicción más reciente del usuario
        prediction = DropoutPrediction.objects.filter(user=user).order_by('-created_at').first()
        
        if not prediction:
            return None
        
        # Obtener características del estudiante si existen
        characteristics = None
        try:
            characteristics = StudentCharacteristics.objects.get(user=user)
        except StudentCharacteristics.DoesNotExist:
            pass
        
        # Construir el contexto formateado
        context_parts = []
        context_parts.append(f"Riesgo de Deserción: {prediction.risk_percentage:.2f}% ({prediction.risk_level})")
        context_parts.append(f"Predicción: {prediction.prediction_label}")
        
        if characteristics and characteristics.course:
            context_parts.append(f"Curso: {characteristics.course.nombre} (Código: {characteristics.course.codigo})")
        
        if characteristics:
            context_parts.append(f"Edad al momento de inscripción: {characteristics.age_at_enrollment} años")
            if characteristics.scholarship_holder:
                context_parts.append("Tiene beca")
            if characteristics.debtor:
                context_parts.append("Tiene deudas pendientes")
            if not characteristics.tuition_fees_up_to_date:
                context_parts.append("Matrícula no está al día")
        
        return "\n".join(context_parts)
        
    except Exception as e:
        # Si hay algún error, no fallar, solo no incluir contexto
        return None

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """
    API endpoint para enviar mensajes al chatbot
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'El mensaje no puede estar vacío'
            })
        
        # Verificar si la API key está configurada
        if not os.getenv('GEMINI_API_KEY'):
            return JsonResponse({
                'success': False,
                'error': 'API key de Gemini no configurada'
            })
        
        # Obtener contexto de predicción si el usuario está autenticado
        prediction_context = None
        if request.user.is_authenticated:
            prediction_context = get_prediction_context(request.user)
        
        # Crear cliente de Gemini y generar respuesta
        try:
            gemini_client = GeminiClient()
            bot_response = gemini_client.chat(user_message, prediction_context=prediction_context)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al conectar con Gemini: {str(e)}'
            })
        
        # Guardar en la base de datos
        chat_message = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_message=user_message,
            bot_response=bot_response,
            model_used="gemini-2.5-flash-lite"
        )
        
        return JsonResponse({
            'success': True,
            'response': bot_response,
            'message_id': chat_message.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })

class ChatHistoryView(TemplateView):
    """
    Vista para mostrar el historial de conversaciones usando el layout de Materio
    """
    template_name = "chatbot_history.html"
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        messages = ChatMessage.objects.all()[:50]  # Últimos 50 mensajes
        context['messages'] = messages
        return context