from rest_framework import serializers

from chat.models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    advertisement = serializers.CharField(source='advertisement.title')

    class Meta:
        model = ChatRoom
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'chat', 'message']


