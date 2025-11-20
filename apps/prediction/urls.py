from django.urls import path
from . import views

app_name = 'prediction'

urlpatterns = [
    path('api/predict-dropout-risk/', views.predict_dropout_risk, name='predict_dropout_risk'),
]

