from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from api_auth.serializers.auth_serializers import RegisterSerializer, UserSerializer
from api_auth.serializers.token_serializers import TokenObtainSerializer, AccessTokenObtainSerializer
from api_auth.tokens import TokenError

MyUser = get_user_model()


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_mail(
            subject="Email address confirmation at Zmall",
            message="",
            html_message=render_to_string('email-confirmation.html',
                                          {'token': str(user.id) + '-' + default_token_generator.make_token(user)}),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[serializer.validated_data['email']],
            fail_silently=False,
        )

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "detail": "User Created Successfully. Check your email account to "
                      "activate the account",
        }, status=status.HTTP_201_CREATED)


class TokenObtainView(generics.GenericAPIView):
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(generics.GenericAPIView):
    serializer_class = AccessTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):

    def post(self, request, *args, **kwargs):
        user_id, token = self.kwargs['key'][0], self.kwargs['key'][2:]
        user = MyUser.objects.get(id=user_id)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response('Email verified successfully.', status=status.HTTP_200_OK)
        return Response('Token is invalid or expired. Please request another confirmation email.',
                        status=status.HTTP_400_BAD_REQUEST)

