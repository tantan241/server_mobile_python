from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.Serializer):
    # def validate_password(self, value):
    #     if len(value) < 4:
    #         return serializers.ValidationError('Mật khẩu phải lớn hơn 5 kí tự')
    #     return value

    # class Meta:
    #     model = CustomUser
    #     fields = ('username','password','email',)
       
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)
    fullName =serializers.CharField(required=True)

class GetUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)