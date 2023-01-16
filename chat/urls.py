<<<<<<< HEAD
from django.urls import path, include
from .views import MessageAPIView, ChatRoomListAPIView, ChatRoomDetailAPIView

urlpatterns = [
    path('room-list/', ChatRoomListAPIView.as_view(), name='chat-room-list'),
    path('room/', ChatRoomDetailAPIView.as_view(), name='chat-room'),
    path('messages/', MessageAPIView.as_view(), name='messages')
]
=======
from django.urls import path, re_path
from chat import views

urlpatterns = [
    re_path(r'message/', views.MessageSendAPIView.as_view(), name='message'),
]
>>>>>>> 420f9660c278aebed21a2a8f1ca5ce670068b81c
