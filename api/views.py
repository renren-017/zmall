from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from api.serializers.serializers import RegisterSerializer, UserSerializer
from api.serializers.token_serializers import TokenObtainSerializer, AccessTokenObtainSerializer
from api.tokens import TokenError

MyUser = get_user_model()


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        }, status=status.HTTP_201_CREATED)


class TokenObtainView(generics.GenericAPIView):
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise ValueError(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(generics.GenericAPIView):
    serializer_class = AccessTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise ValueError(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)