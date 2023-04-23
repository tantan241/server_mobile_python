from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.Serializer):     
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)
    fullName =serializers.CharField(required=True)

class GetUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password =serializers.CharField(required=True)

#admin
class GetCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
class GetCustomerAdminSerializers(serializers.Serializer):
    limit = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=True)
    search = serializers.DictField(required=False)
    sort = serializers.DictField(required=False)