from rest_framework import serializers

from chat.models import ChatRoom, Message, User


class MessageSerializer(serializers.ModelSerializer):
    # advertisement = serializers.IntegerField()
    sender = serializers.CharField(source='sender.pk', read_only=True)
    is_read = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'receiver', 'sender', 'date_of_send', 'is_read', 'message']
        extra_kwargs = {"message": {"required": False}}


class ChatRoomListSerializer(serializers.ModelSerializer):
    message_channels = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'advertisement', 'message_channels']


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.id')
    receiver = serializers.CharField(source='advertisement.owner.id')

    class Meta:
        model = ChatRoom
        fields = ['id', 'advertisement', 'sender', 'receiver']






