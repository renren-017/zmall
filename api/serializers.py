from rest_framework import  serializers
from django.contrib.auth import get_user_model

MyUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], password=validated_data['password'],
                                          first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
