from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AddCartSerializers, GetCartSerializers, UpdateNumberSerializers, DeleteCartDetailSerializers,GetNumberProductSerializers
from rest_framework.response import Response
from rest_framework import status, generics
from .models import CartDetail, Cart
from apps.product.models import Product
from apps.user.models import User
# Create your views here.

# class CreateCartView(APIView):
#     def post(self,request):
#         data = CreateCartSerializers(data=request.data)
#         if not data.is_valid():
#             return Response("Lỗi dữ liệu đầu vào tạo cart.",status=status.HTTP_400_BAD_REQUEST)
#         print(data)
#         return Response("Ok",status=status.HTTP_200_OK)


class AddCartView(APIView):
    def post(self, request):
        data = AddCartSerializers(data=request.data)
        if not data.is_valid():
            return Response("Lỗi dữ liệu đầu vào thêm sản phẩm.", status=status.HTTP_400_BAD_REQUEST)
        cartOfUser = Cart.objects.filter(user=data.data["user"]).first()      
        if not cartOfUser:
            user = User.objects.get(id = data.data["user"])
            Cart.objects.create(user= user)
            cartOfUser = Cart.objects.filter(user=data.data["user"]).first()  
        productOfCart = Product.objects.filter(pk=data.data["product"]).first()
        if cartOfUser and productOfCart:
            checkCartDetail = CartDetail.objects.filter(
                cart=cartOfUser, product=data.data["product"]).first()
            if checkCartDetail:
                number = checkCartDetail.number + 1

                CartDetail.objects.filter(
                    cart=cartOfUser, product=data.data["product"]).update(number=number)
                return Response({"status": 200,
                                 "messenger": "Update thành công"}, status=status.HTTP_200_OK)
            CartDetail.objects.create(cart=cartOfUser, product=productOfCart,
                                      number=data.data["number"], price=data.data["price"])
        else:
            return Response("Người dùng hoặc sản phẩm không tồn tại.", status=status.HTTP_200_OK)
        return Response({"status": 200,
                         "messenger": "Thêm thành công"}, status=status.HTTP_200_OK)


class GetCartView(generics.ListAPIView):
    def get(self, request):
        id = request.GET.get("id")
        cart = Cart.objects.filter(user=id).first()
        listCartDetail = CartDetail.objects.filter(cart=cart)
        res = GetCartSerializers(listCartDetail, many=True)
        return Response({"status": 200,
                         "messenger": "Lấy dữ liệu thành công",
                         "data": res.data
                         }, status=status.HTTP_200_OK)


class UpdateNumberView(APIView):
    def post(self, request):
        data = UpdateNumberSerializers(data=request.data)
        if not data.is_valid():
            return Response("Lỗi dữ liệu đầu vào")
        try:
            cart = Cart.objects.get(user=data.data["userId"])
        except:
            return Response("Không tồn tại user")
        try:
            cartDetail = CartDetail.objects.filter(
                cart=cart, product=data.data["productId"])
            number = cartDetail.first().number
            if data.data["type"] == 0:
                number -= 1
            elif data.data["type"] == 1:
                number += 1
            print(number)

            cartDetail.update(number=number)
            return Response({"status": 200, "messenger": "Update số lượng thành công", "data": {
                "number": number
            }}, status=status.HTTP_200_OK)
        except:
            return Response("Không tồn tại chi tiết giỏ hàng")


class DeleteCartDetailView(APIView):
    def post(self, request):
        data = DeleteCartDetailSerializers(data=request.data)
        if not data.is_valid():
            return Response("Lỗi dữ liệu đầu vào")
        try:
            cart = Cart.objects.get(user=data.data["userId"])
        except:
            return Response("Không tồn tại user")
        try:
            cartDetail = CartDetail.objects.filter(
                cart=cart, product=data.data["productId"]).first()
            cartDetail.delete()
            return Response({"status": 200, "messenger": "Xóa thành thành công!"}, status=status.HTTP_200_OK)
        except:
            return Response("Không tồn tại chi tiết giỏ hàng")

class DeleteCartView(APIView):
    def delete(self, request):
        userId = request.query_params.get('userId')
        try:
            cart = Cart.objects.get(user=userId)                  
            CartDetail.objects.filter(cart_id=cart.id).delete()
            cart.delete()
        except:
             return Response({"status":400,
                                 "messenger": "Người dùng chưa có giỏ hàng"})
        return Response({"status": 200})