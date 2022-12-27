from django.contrib.auth import authenticate
from rest_framework import serializers

from api_auth.tokens import RefreshToken, AccessToken, decode_jwt


class TokenObtainSerializer(serializers.Serializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField()

    def validate(self, attrs):

        authenticate_kwargs = {
            "email": attrs["email"],
            "password": attrs["password"],
        }

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            raise KeyError("Request not found")

        self.user = authenticate(**authenticate_kwargs)

        try:
            refresh = self.get_token(self.user.id)
        except AttributeError:
            raise AttributeError("Request: {}. User with email {} and password {} could not authenticate".format(
                authenticate_kwargs['request'], attrs["email"], attrs["password"]
            ))
        print("Request: {}. User with email {} and password {} authenticated".format(
            authenticate_kwargs['request'], attrs["email"], attrs["password"]
        ))
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data

    @classmethod
    def get_token(cls, user_id):
        return cls.token_class.create(user_id)


class AccessTokenObtainSerializer(serializers.Serializer):
    token_class = AccessToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['refresh'] = serializers.CharField()

    def validate(self, attrs):
        token = decode_jwt(attrs["refresh"])
        token_class = RefreshToken(token=token)
        refresh = token_class.create(token['user'])
        data = {"access": str(refresh.access_token)}

        return data
