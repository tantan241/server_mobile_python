from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.Serializer):     
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)
    fullName =serializers.CharField(required=True)

class GetUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)