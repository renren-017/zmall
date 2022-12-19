from django.urls import path, include
from .views import MessageAPIView

urlpatterns = [
    path('messages/', MessageAPIView.as_view(), name='messages')
]
