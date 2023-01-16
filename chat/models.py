from django.contrib.auth import get_user_model
from django.db import models

from advertisement.models import Advertisement

User = get_user_model()


class ChatRoom(models.Model):
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='take_room')
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='send_room')
    advertisement = models.ForeignKey(to=Advertisement, on_delete=models.CASCADE)


class Message(models.Model):
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='took_messages')
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sent_messages')
    chat = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name='message_channels')
    message = models.TextField(max_length=2000, blank=True)
    date_of_send = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
