from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from .serializers import CreateOrderSerializers
from .models import Order,OrderMethod,OrderDetail
from apps.user.models import CustomUser
from apps.product.models import Product
import json
# Create your views here.
class CreateOrderView(APIView):
    def post(self, request, *args, **kwargs):
        
        data = CreateOrderSerializers(data = request.data)
       
        if not data.is_valid():
            return Response({"messenger": "Lỗi",
                             "status": 400},status=status.HTTP_400_BAD_REQUEST) 
        order_method = OrderMethod.objects.get(id=data.data["order_method"])
        custom_user = CustomUser.objects.get(id=data.data["user"])
        order = Order.objects.create(order_method= order_method,user = custom_user,name = data.data["name"], phone =data.data["phone"], address = data.data["address"],note=data.data["note"],email = data.data["email"],totalMoney = data.data["totalMoney"],)
        
        orderDetail = list()
        for item in data.data["order_detail"] :
            draft = dict()
            draft["order"] =  order.id
            draft["product"] =  item["product"] 
            draft["number"] =  item["number"] 
            draft["price"] =  item["price"] 
            orderDetail.append(draft)
        for item in orderDetail:
            product = Product.objects.get(id=item["product"])
            OrderDetail.objects.create(order = order,product = product, number = item["number"], price = item["price"])
        return Response({"status": 200,
                         "messenger": "Đặt hàng thành công",
                         "data": {"id": order.id}
                         })
