from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.pusher import pusher_client
from .models import Message
from .serializers import MessageSerializer


class MessageAPIView(CreateAPIView):
    model = Message
    serializer_class = MessageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        pusher_client.trigger('chat', 'message', {
            'username': request.user.username,
            'message': request.data['message']
        })
        return Response('message sent')


class MessageListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
