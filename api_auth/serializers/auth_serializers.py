import re
from rest_framework import serializers
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], password=validated_data['password'],
                                          first_name=validated_data['first_name'],
                                          last_name=validated_data['last_name'])
        return user

    def validate(self, attrs):
        pass_pattern = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        name_pattern = "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"

        if not re.match(name_pattern, attrs['first_name']) or not re.match(name_pattern, attrs['last_name']):
            raise serializers.ValidationError('Your name can consist only of letters and \'-. characters.')

        if not re.match(pass_pattern, attrs['password']):
            raise serializers.ValidationError('Your password should consist of minimum 8 characters, '
                                              'at least 1 letter and 1 number.')

        return attrs


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', 'password')

    def is_valid(self, *, raise_exception=False):
        # Checking if entered credentials are valid

        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active',)
