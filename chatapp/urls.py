from django.urls import path, include
from .views import inbox, chat_detail, chat_create

urlpatterns = [
    path('chats/', inbox, name='inbox'),
    path('chat/<int:pk>/', chat_detail, name="chat_detail"),
    path('chat/new/', chat_create, name="chat_create"),
]