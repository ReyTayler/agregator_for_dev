from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.analyze_resume, name='ai_analyze'),
]