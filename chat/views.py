<<<<<<< HEAD
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.pusher import pusher_client
from .models import Message, ChatRoom
from .notification import notification
from .serializers import MessageSerializer, ChatRoomListSerializer, ChatRoomDetailSerializer


class ChatRoomListAPIView(ListAPIView):
    model = ChatRoom
    serializer_class = ChatRoomListSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        receiver = Q(advertisement__owner=self.request.user)
        sender = Q(message_channels__sender=self.request.user)
        return ChatRoom.objects.filter(receiver | sender).distinct()


class MessageAPIView(CreateAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(request_body=MessageSerializer(many=True), operation_description='Send message')
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        messages = serializer.save()
        notification(messages.receiver)
        data = {
            'message': messages.message, 'sender': messages.sender,
            'receiver': messages.receiver, 'date_of_send': messages.date_of_send
        }

        pusher_client.trigger(f"{messages.chat.id}", 'message', data)
        return Response(data, status=status.HTTP_201_CREATED)


class ChatRoomDetailAPIView(RetrieveAPIView):
    model = ChatRoom
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomDetailSerializer
    parser_classes = (MultiPartParser, FormParser)
    chat_id = openapi.Parameter('chat_id', openapi.IN_QUERY, description='chat id', type=openapi.TYPE_STRING)

    @swagger_auto_schema(responses={200: ChatRoomDetailSerializer(many=True)}, manual_parameters=(chat_id, ))
    def get(self, request, *args, **kwargs):
        chat_id = request.query_params.get('chat_id')
        chat = get_object_or_404(ChatRoom, id=chat_id)
        user = request.user
        Message.objects.filter(chat=chat)
        data = Message.objects.filter(Q(reciever=user, chat=chat) | Q(sender=user, chat=chat))
        serializer = MessageSerializer(data, many=True)
        is_read_messages = Message.objects.exclude(sender=request.user.pk)
        is_read_messages.filter(chat=chat, is_read=False).update(is_read=True)
        response_body = {
            'chat': chat,
            'message': serializer.data,
            'advertisement': chat.advertisement.id,
            'sender': chat.sender.id,
            'receiver': chat.receiver.id,
        }
        return Response(response_body)
=======
import asyncio

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from chat.models import Message
from chat.serializers import MessageSerializer


class MessageSendAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "general", {"type": "send_info_to_user_group",
                        "text": {"status": "done"}}
        )

        return Response({"status": True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=MessageSerializer)
    def post(self, request):
        msg = Message.objects.create(user=request.user, message=request.data["message"])
        socket_message = f"Message with id {msg.id} was created!"
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{request.user.id}-message", {"type": "send_last_message",
                                           "text": socket_message}
        )

        return Response({"status": True}, status=status.HTTP_201_CREATED)

>>>>>>> 420f9660c278aebed21a2a8f1ca5ce670068b81c
