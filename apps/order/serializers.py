from rest_framework import serializers
from .models import Order,OrderDetail
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
        fields =('order_method','user','name','phone','email','address','note','order_detail','totalMoney')
        # fields = "__all__"