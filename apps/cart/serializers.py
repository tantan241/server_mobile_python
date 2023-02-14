from rest_framework import serializers
from .models import CartDetail,Cart

# class CreateCartSerializers(serializers.ModelSerializer):
#     class Meta:
#         model= Cart
#         fields= "__all__"
class AddCartSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField()
    class Meta:
        model= CartDetail
        fields= ("user","product","number","price")
class GetCartSerializers(serializers.ModelSerializer):
    name = serializers.CharField(read_only= True,source ="product.name")
    image = serializers.CharField(read_only= True,source ="product.image")
    discount = serializers.IntegerField(read_only= True,source ="product.discount")
    price = serializers.IntegerField(read_only= True,source ="product.price")
    class Meta:
        model= CartDetail
        fields =("cart","product","number","price","name","image","discount","price")


class UpdateNumberSerializers(serializers.Serializer):
    userId = serializers.IntegerField()
    type = serializers.IntegerField()
    productId = serializers.IntegerField()
class DeleteCartDetailSerializers(serializers.Serializer):
    userId = serializers.IntegerField()
    productId = serializers.IntegerField()