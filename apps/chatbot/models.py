from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    """
    Modelo para almacenar mensajes del chatbot
    """
    user_message = models.TextField(verbose_name="Mensaje del usuario")
    bot_response = models.TextField(verbose_name="Respuesta del bot")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    model_used = models.CharField(max_length=100, default="gemini-2.5-flash-lite", verbose_name="Modelo utilizado")
    
    class Meta:
        verbose_name = "Mensaje de Chat"
        verbose_name_plural = "Mensajes de Chat"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"