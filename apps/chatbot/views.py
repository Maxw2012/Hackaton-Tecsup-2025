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

class ChatView(TemplateView):
    """
    Vista principal del chatbot usando el layout de Materio
    """
    template_name = "chatbot_chat.html"
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

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
        
        # Crear cliente de Gemini y generar respuesta
        try:
            gemini_client = GeminiClient()
            bot_response = gemini_client.chat(user_message)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al conectar con Gemini: {str(e)}'
            })
        
        # Guardar en la base de datos
        chat_message = ChatMessage.objects.create(
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