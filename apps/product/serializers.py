from rest_framework import serializers
from .models import Brand,Product,ProductVariant
class GetBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Brand
        fields= "__all__"

class GetProductSerializer(serializers.Serializer):
    filter = serializers.DictField()
    type = serializers.IntegerField(required=False)
    price = serializers.DictField(required=False)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Product
        fields= '__all__'

# class GetProductDetailsSerializer(serializers.ModelSerializer):
#     name =serializers.CharField(read_only=True,source="product.name")
#     slug =serializers.CharField(read_only=True,source="product.slug")
#     price =serializers.IntegerField(read_only=True,source="product.price")
#     discount =serializers.IntegerField(read_only=True,source="product.discount")
#     type =serializers.IntegerField(read_only=True,source="product.type")
#     image =serializers.CharField(read_only=True,source="product.image")
#     # status =serializers.IntegerField(read_only=True,source="product.status")
#     brand =serializers.CharField(read_only=True,source="product.brand")

#     class Meta:
#         model = ProductDetail
#         fields = ('id','display','system','frontCamera','rearCamera','chip','ram','rom','battery','name','slug','price',
#         'discount','type','image','brand')
class GetProductDetailsSerializer(serializers.ModelSerializer):
    type =serializers.IntegerField(read_only=True,source="product.type")
    brand =serializers.CharField(read_only=True,source="product.brand")
    name =serializers.CharField(read_only=True,source="product.name")

    class Meta:
        model = ProductVariant
        fields = ('id','images','name','slug','price',
        'discount','type','image','brand','specifications')
