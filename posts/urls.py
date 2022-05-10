from django.urls import path
from .views import (
    welcome, 
    feed, 
    contact, 
    post_create, 
    post_detail, 
    post_update, 
    post_delete
    )




urlpatterns = [
    path('', welcome, name='welcome'),
    path('feed/', feed, name='feed'),
    path('contact/', contact, name='contact'),
    path('post/new/', post_create, name='post_create'),
    path('post/detail/<int:pk>/', post_detail, name='post_detail'),
    path('post/update/<int:pk>/', post_update, name='post_update'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
]