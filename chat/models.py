from django.contrib.auth import get_user_model
from django.db import models

from advertisement.models import Advertisement

User = get_user_model()


class ChatRoom(models.Model):
    advertisement = models.ForeignKey(to=Advertisement, on_delete=models.CASCADE, related_name='chat_rooms')


class Message(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='messages')
    chat = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField(max_length=2000, blank=True)
