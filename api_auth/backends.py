import jwt
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

from api_auth.tokens import decode_jwt

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):

        try:
            payload = decode_jwt(token)
        except Exception:
            raise exceptions.AuthenticationFailed('Authentication error. Cannot decode token')

        try:
            user = User.objects.get(pk=payload['user'])
        except User.DoesNotExist:
            msg = 'User not found'
        if not user.is_active:
            msg = 'User is not active'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
