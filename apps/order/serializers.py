from rest_framework import serializers
from .models import Order, OrderDetail
from apps.cart.models import CartDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = ('order', 'product', 'price', "number")
        # fields = "__all__"


class CreateOrderSerializers(serializers.ModelSerializer):
    order_detail = serializers.JSONField()

    class Meta:
        model = Order
        fields = ('order_method', 'user', 'name', 'phone', 'email',
                  'address', 'note', 'order_detail', 'totalMoney')
        # fields = "__all__"


class GetOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
class GetOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"

# admin
class GetListOrderAdminSerializers(serializers.Serializer):
    limit = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=True)
    search = serializers.DictField(required=False)
    sort = serializers.DictField(required=False)

class AddOrderAdminSerializer(serializers.Serializer):
    name= serializers.CharField(required=True)
    email= serializers.EmailField(required=True)
    phone= serializers.CharField(required=True)
    address= serializers.CharField(required=True)
    note= serializers.CharField(required=False)
    createdAt= serializers.DateTimeField(required=True)
    status =serializers.IntegerField(required=True)
    id =serializers.IntegerField(required=False)
    user =serializers.IntegerField(required=True)
    order_method =serializers.IntegerField(required=True)
    orderDetail = serializers.ListField(required=False)
    totalMoney =serializers.DecimalField(required=True,max_digits=15, decimal_places=2)
