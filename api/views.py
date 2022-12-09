from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer

MyUser = get_user_model()


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)