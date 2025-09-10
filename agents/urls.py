from django.urls import path
from . import views

app_name = 'agents'
urlpatterns = [
    path('ai-assistant/', views.ai_assistant_page, name='ai_assistant_page'),
    path('ask-ai/', views.ask_ai, name='ask_ai'),
    path('clear-history/', views.clear_ai_history, name='clear_ai_history'),
]