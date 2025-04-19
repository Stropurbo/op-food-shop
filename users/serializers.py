from django.shortcuts import render, redirect,HttpResponse,get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import CustomUser


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number']

class CurrentUserSerializers(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number']




