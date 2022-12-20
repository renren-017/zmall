from django.contrib.auth import authenticate
from rest_framework import serializers


from ..tokens import RefreshToken, AccessToken, decode_jwt


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
            pass

        self.user = authenticate(**authenticate_kwargs)

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class AccessTokenObtainSerializer(serializers.Serializer):
    token_class = AccessToken
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['refresh'] = serializers.CharField()

    def validate(self, attrs):

        refresh = decode_jwt(attrs["refresh"])
        data = {"access": str(refresh.access_token)}

        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.create(user)
