from django.urls import path, include
from .views import MessageAPIView, ChatRoomListAPIView, ChatRoomDetailAPIView

urlpatterns = [
    path('room-list/', ChatRoomListAPIView.as_view(), name='chat-room-list'),
    path('room/', ChatRoomDetailAPIView.as_view(), name='chat-room'),
    path('messages/', MessageAPIView.as_view(), name='messages')
]
