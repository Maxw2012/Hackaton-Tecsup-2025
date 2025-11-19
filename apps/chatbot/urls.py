from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chatbot/', views.ChatView.as_view(), name='chat'),
    path('chatbot/send/', views.send_message, name='send_message'),
    path('chatbot/history/', views.ChatHistoryView.as_view(), name='history'),
]
