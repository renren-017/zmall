from django.db.models import Q
from chat.models import ChatRoom, Message
from chat.pusher import pusher_client


def notification(user):
    chat_rooms = ChatRoom.objects.filter(Q(receiver=user) | Q(sender=user))
    data = {}
    for chat in chat_rooms:
        data[chat] = Message.objects.filter(reciever=user, is_read=False, chat=chat).count()
    data['all'] = Message.objects.filter(receiver=user, is_read=False).count()
    pusher_client.trigger("notifications", "notification", data)
