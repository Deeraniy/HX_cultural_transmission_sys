from django.urls import path
from .views import gradio_view, chat

urlpatterns = [
    path('gradio/', gradio_view, name='gradio_view'),
    path('chat/', chat, name='chat'),
] 