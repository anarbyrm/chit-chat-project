from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

User = settings.AUTH_USER_MODEL



class Chat(models.Model):
    chat_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_sender')
    chat_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_receiver')
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-date']


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_sender')
    message_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_receiver')
    body = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-date']