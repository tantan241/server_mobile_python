from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import UserSerializer, GetUserSerializer
from .models import CustomUser
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from apps.cart.models import Cart
# Create your views here.


class Demo(View):
    def get(self, request):
        return HttpResponse("hello word")


# class MyTokenObtainPairView(TokenObtainPairView):
#     def get_user(self, validated_data):
#         user_queryset = User.objects.filter(idGoogle=validated_data['idGoogle'])
#         user = user_queryset.first()
#         # if not user:
#         #     user = User.objects.create(idGoogle=validated_data['idGoogle'])
#         return user


class CreateUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        data = UserSerializer(data=request.data)
        try:
            if not data.is_valid():
                return Response({"status": 400,
                                "data": "Lỗi dữ liệu"}, status=status.HTTP_400_BAD_REQUEST)
            username = (data.data)["username"]
            checkUsername = CustomUser.objects.filter(username=username)
            if checkUsername.exists():
                return Response({"status": 400,
                                "data": "Lỗi dữ liệu",
                                 "messenger": "Tài khoản đã tồn tại."

                                 }, status=status.HTTP_200_OK)
            fullName = (data.data)["fullName"]
            password = make_password((data.data)["password"])
            user = CustomUser.objects.create(
                username=username, password=password, fullName=fullName)
            Cart.objects.create(user=user)
            return JsonResponse({"status": 200,
                                "data": f"{data.data}",
                                 "messenger": "Tạo mới tài khoản thành công."}, status=status.HTTP_201_CREATED)
        except EOFError:
            return Response({"status": 400,
                             "data": "Lỗi dữ liệu",
                             "messenger": "Tài khoản đã tồn tại."

                             }, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        dataGet = GetUserSerializer(data=request.data)
        if not dataGet.is_valid():
            return Response({"status": 400,
                            "data": f"Lỗi dữ liệu"}, status=status.HTTP_400_BAD_REQUEST)
        username = (dataGet.data)["username"]
        password = ((dataGet.data)["password"])
        checkUserName = CustomUser.objects.filter(username=username)
        if (not checkUserName):
            return JsonResponse({"status": 400,
                                 "messenger": "Tài khoản chưa chính xác"})
        passWordDb = (CustomUser.objects.get(username=username)).password
        checkPassWord = check_password(password, passWordDb)
        if not checkPassWord:
            return JsonResponse({"status": 400,
                                 "messenger": "Mật khẩu chưa chính xác"})
        user = CustomUser.objects.get(username=username)
        return JsonResponse({"status": 200,
                             "messenger": "Đăng nhập thành công",
                             "data": {"fullName": user.fullName,
                                      "id": user.id}})
