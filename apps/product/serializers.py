from rest_framework import serializers
from .models import Brand, Product
from apps.comment.models import Comment


class GetBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class GetProductSerializer(serializers.Serializer):
    filter = serializers.DictField()
    type = serializers.IntegerField(required=False)
    price = serializers.DictField(required=False)
    order = serializers.CharField(required=False, allow_blank=True)
    page = serializers.IntegerField(required=True)  # số page
    numberProduct = serializers.IntegerField(
        required=True)  # số sản phẩm trả về trong 1 page


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # fields= ('id', 'name', 'type','status', 'brand', 'slug', 'price','discount','image','images','number','specification','')

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
    class Meta:
        model = Product
        fields = "__all__"


class GetRoleReviewProductSerializers(serializers.Serializer):
    userId = serializers.IntegerField(required=True)
    productId = serializers.IntegerField(required=True)


class CompareProductSerializers(serializers.Serializer):
    productId1 = serializers.IntegerField(required=True)
    productId2 = serializers.IntegerField(required=True)

# admin


class GetBrandAdminSerializers(serializers.Serializer):
    limit = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=True)
    search = serializers.DictField(required=False)
    sort = serializers.DictField(required=False)


class GetListProductAdminSerializers(serializers.Serializer):
    limit = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=True)
    search = serializers.DictField(required=False)
    sort = serializers.DictField(required=False)


class AddBrandSerializers(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.IntegerField(required=True)
    id = serializers.IntegerField(required=False)
