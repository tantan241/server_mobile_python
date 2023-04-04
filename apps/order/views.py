from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import CreateOrderSerializers, GetOrderSerializer
from apps.product.serializers import ProductSerializer
from .models import Order, OrderMethod, OrderDetail
from apps.user.models import CustomUser
from apps.product.models import Product
import json
# Create your views here.


class CreateOrderView(APIView):
    def post(self, request, *args, **kwargs):

        data = CreateOrderSerializers(data=request.data)

        if not data.is_valid():
            return Response({"messenger": "Lỗi",
                             "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        order_method = OrderMethod.objects.get(id=data.data["order_method"])
        custom_user = CustomUser.objects.get(id=data.data["user"])
        order = Order.objects.create(order_method=order_method, user=custom_user, name=data.data["name"], phone=data.data[
                                     "phone"], address=data.data["address"], note=data.data["note"], email=data.data["email"], totalMoney=data.data["totalMoney"],)

        orderDetail = list()
        for item in data.data["order_detail"]:
            draft = dict()
            draft["order"] = order.id
            draft["product"] = item["product"]
            draft["number"] = item["number"]
            draft["price"] = item["price"]
            orderDetail.append(draft)
        for item in orderDetail:
            product = Product.objects.get(id=item["product"])
            OrderDetail.objects.create(
                order=order, product=product, number=item["number"], price=item["price"])
        return Response({"status": 200,
                         "messenger": "Đặt hàng thành công",
                         "data": {"id": order.id}
                         })


class CountOrderView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.GET["user"]
        user = CustomUser.objects.get(id=user_id)
        count_order = Order.objects.filter(
            user=user, status=0).count()  # 1 đang thực hiện
        return Response({"status": 200, "count": count_order})


class GetListOrder(APIView):
    def get(self, request, *args, **kwargs):
        userId = request.GET.get('userId')
        user = ""
        try:
            user = CustomUser.objects.get(id=userId)
        except:
            return Response({"status": 400, "messenger": "Không tồn tại user"}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(user=user).order_by("-createdAt")
        data = GetOrderSerializer(orders, many=True)
        data_response = list()
        for order in data.data:
            count = OrderDetail.objects.filter(
                order_id=order["id"]).count()
            order["count"] = count
            data_response.append(order)
        return Response({"status": 200, "data": data_response})

class GetOrderDetail(APIView):
    def post(self, request):
        order_id = request.data['orderId']
       
        try:
            order = Order.objects.get(id=order_id)
            orderRes = GetOrderSerializer(order)
            orderDetail = OrderDetail.objects.filter(order=order).values()
            listOrderDetail = list()
            for item in orderDetail :
                product_query = Product.objects.get(id=item["product_id"])
                product = ProductSerializer(product_query)
                print(product.data)
                item["image"] = product.data["image"]
                item["name"] = product.data["name"]
                product_specifications = product.data["specifications"]
                ram =""
                rom =""
                for it in product_specifications:
                    if it["name"] =="ram":
                        ram= it["value"]
                    if it["name"] =="rom":
                        rom = it["value"]
                specifications = ram +"-"+ rom
                item["specifications"] = specifications
                listOrderDetail.append(item)
            res =orderRes.data
            
            res["orderDetail"] =listOrderDetail
            return Response({"status": 200, "data": res})
        except:
            return  Response({"status":400,"messenger": "Lỗi"},status=status.HTTP_400_BAD_REQUEST)