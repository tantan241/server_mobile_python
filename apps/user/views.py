from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import UserSerializer, GetUserSerializer,GetCustomerAdminSerializers,GetCustomerSerializer,AddCustomerSerializers
from .models import CustomUser
from django.contrib.auth.models import User, AnonymousUser
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from apps.cart.models import Cart
from django.db.models import Q
from apps.order.models import Order
from django.db.models import Sum
import json
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

# admin


class LoginAdmin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        dataGet = GetUserSerializer(data=request.data)
        if not dataGet.is_valid():
            return Response({"status": 400,
                            "data": f"Lỗi dữ liệu"}, status=status.HTTP_400_BAD_REQUEST)
        username = (dataGet.data)["username"]
        password = ((dataGet.data)["password"])
        checkUserName = User.objects.filter(username=username)
        if (not checkUserName):
            return JsonResponse({"status": 400,
                                 "messenger": "Tài khoản chưa chính xác"})
        passWordDb = (User.objects.get(username=username)).password
        checkPassWord = check_password(password, passWordDb)
        if not checkPassWord:
            return JsonResponse({"status": 400,
                                 "messenger": "Mật khẩu chưa chính xác"})
        user = User.objects.get(username=username)
        if not user.is_superuser:
            return JsonResponse({"status": 400,
                                 "messenger": "Bạn không có quyền vào trang này",
                                 "data": {
                                 }})
        name = user.first_name + " " + user.last_name
        return JsonResponse({"status": 200,
                             "messenger": "Đăng nhập thành công",
                             "data": {"fullName": name,
                                      }})


class GetCustomerAdminView(APIView):
    def post(self, request):
        fields = ["name", "status"]
        columns = [
            {"field": "stt", "headerName": "STT",
                "sortable": False,  "flex": 0.2, "filterable": False},
            {"field": "fullName", "headerName": "Họ và tên", "sortable": False,
                "filterable": False, "flex": 1},
            {"field": "address", "headerName": "Địa chỉ", "sortable": False,
             "filterable": False, "flex": 1},
            {"field": "phone", "headerName": "Số điện thoại", "sortable": False,
             "filterable": False, "flex": 1},
              {"field": "emailCustomer", "headerName": "Email", "sortable": False,
             "filterable": False, "flex": 1},
            # {"field": "status", "headerName": "Trạng Thái",
            #     "filterable": False, "flex": 1, "sortable": False},
        ]
        dataSearch = [
            {
                "name": "--- Chọn giá trị ---",
                "value": "default",
                "type": "",
            },
            {
                "name": "Họ và tên",
                "value": "fullName",
                "type": "text",
            },
            {
                "name": "Địa chỉ",
                "value": "address",
                "type": "text",
            },
            {
                "name": "Số điện thoại",
                "value": "phone",
                "type": "text",
            },
             {
                "name": "Email",
                "value": "emailCustomer",
                "type": "text",
            },
            # {
            #     "name": "Trạng thái",
            #     "value": "status",
            #     "type": "select",
            #     "select": [
            #         {
            #             "name": "--- Chọn giá trị ---",
            #             "value": "default",
            #         },
            #         {
            #             "name": "Hoạt động",
            #             "value": "1",
            #         },
            #         {
            #             "name": "Ngừng Hoạt động",
            #             "value": "0",
            #         },
            #     ],
            # }
        ]
        dataFilter = [
            {"name": "Họ và tên",
             "value": "fullName"},
            #  {"name": "Họ và tên",
            #  "value": "fullName"},

        ]
        data = GetCustomerAdminSerializers(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dữ liệu đầu vào"}, status=status.HTTP_400_BAD_REQUEST)
        limit = data.data["limit"]
        page = data.data["page"]
        search = data.data["search"]
        sort = data.data.get("sort")

        q = Q()
        q &= Q(id__gte=0)

        if search["field"] and search["field"] != "default":
            if search["type"] == "text":
                query = f"{search['field']}__icontains"
                q &= Q(**{query: search["value"]})
            if search["type"] == "select" and search["value"] != "default":
                query = f"{search['field']}"
                q &= Q(**{query: search["value"]})
        start = page * limit
        end = start + limit

        if sort and sort["field"] in fields:
            field_order_by = sort["field"]
            if sort["sort"] == "desc":  # giảm dần
                field_order_by = "-" + str(sort["field"])
            data_orm = CustomUser.objects.filter(
                q).order_by(field_order_by)[start:end]
        else:
            data_orm = CustomUser.objects.filter(q)[start:end]
        count = CustomUser.objects.filter(q).count()
        pageInfo = {"limit": limit, "page": page, "count": count}
        data = GetCustomerSerializer(data_orm, many=True)
        index = page * limit + 1
        for item in data.data:
            item["stt"] = index
            index += 1
        return Response({"status": 200, "columns": columns, "rows": data.data, "pageInfo": pageInfo, "dataSearch": dataSearch, "dataFilter": dataFilter})
    def delete(self, request):
        ids_json = request.GET.get('ids')
        ids = json.loads(ids_json)
        if ids and len(ids) > 0:
            User.objects.filter(id__in=tuple(ids)).delete()
            return Response({"status": 200, "messenger": "Xóa thành công"})
        return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"})

class GetOneCustomerView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if not id:
            return Response({"status": 400, "messenger": "Lỗi không tìm thấy id"}, status=status.HTTP_400_BAD_REQUEST)
        customer = CustomUser.objects.get(id=id)
        customer = GetCustomerSerializer(customer)
        data= dict()
        data["fullName"]= customer.data["fullName"]
        data["username"]= customer.data["username"]
        data["id"]= customer.data["id"]
        data["phone"]= customer.data["phone"]
        data["email"]= customer.data["emailCustomer"]
        data["address"]= customer.data["address"]
        order = Order.objects.filter(user_id=id)
        number_order = order.count()
        data["number_order"]= number_order
        total_price = order.aggregate(Sum('totalMoney'))['totalMoney__sum']
        data["total_price"]= total_price
        return Response({"status": 200, "data": data})
   
class AddCustomerView(APIView):
    def post(self, request):
        data = AddCustomerSerializers(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dũ liệu đẩu vào"}, status=status.HTTP_400_BAD_REQUEST)
        fullName = data.data["fullName"]
        email = data.data["email"]
        address = data.data["address"]
        phone = data.data["phone"]
        id = data.data.get("id")
        # status = data.data["status"]
        if id:
            CustomUser.objects.filter(id=id).update(fullName=fullName, emailCustomer=email,address=address,phone=phone)
            return Response({"status": 200, "messenger": "Cập nhâp thành công"})
        CustomUser.objects.create(fullName=fullName, emailCustomer=email,address=address,phone=phone)
        return Response({"status": 200, "messenger": "Thêm mới thành công"})