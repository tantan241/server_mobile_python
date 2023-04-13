from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import CreateOrderSerializers, GetOrderSerializer,GetListOrderAdminSerializers
from apps.product.serializers import ProductSerializer
from .models import Order, OrderMethod, OrderDetail
from apps.user.models import CustomUser
from apps.product.models import Product
import json
from django.db.models import Q
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
            for item in orderDetail:
                product_query = Product.objects.get(id=item["product_id"])
                product = ProductSerializer(product_query)
                item["image"] = product.data["image"]
                item["name"] = product.data["name"]
                product_specifications = product.data["specifications"]
                ram = ""
                rom = ""
                for it in product_specifications:
                    if it["name"] == "ram":
                        ram = it["value"]
                    if it["name"] == "rom":
                        rom = it["value"]
                specifications = ram + "-" + rom
                item["specifications"] = specifications
                item["discount"] = product.data["discount"]
                listOrderDetail.append(item)
            res = orderRes.data

            res["orderDetail"] = listOrderDetail
            return Response({"status": 200, "data": res})
        except:
            return Response({"status": 400, "messenger": "Lỗi"}, status=status.HTTP_400_BAD_REQUEST)

# admin


class GetListOrderAdminView(APIView):
    def post(self, request):
        fields = ["name", "status", "phone", "email",
                  "address", "createdAt", "totalMoney"]
        columns = [
            {"field": "stt", "headerName": "STT",
                "sortable": False,  "flex": 0.2, "filterable": False},
            {"field": "name", "headerName": "Họ Và Tên", "sortable": False,
                "filterable": False, "flex": 1},
            {"field": "phone", "headerName": "Số Điện Thoại",
                "filterable": False, "flex": 1, "sortable": False},
            {"field": "email", "headerName": "Email",
             "filterable": False, "flex": 1, "sortable": False},
            {"field": "address", "headerName": "Địa Chỉ",
             "filterable": False, "flex": 1, "sortable": False},
            {"field": "createdAt", "headerName": "Ngày Lập",
             "filterable": False, "flex": 1, "sortable": False},
            {"field": "totalMoney", "headerName": "Tổng Tiền",
             "filterable": False, "flex": 1, "sortable": False},

        ]
        dataSearch = [
            {
                "name": "--- Chọn giá trị ---",
                "value": "default",
                "type": "",
            },
            {
                "name": "Tên khách hàng",
                "value": "name",
                "type": "text",
            },
            {
                "name": "Số điện thoại",
                "value": "phone",
                "type": "text",
            },
            {
                "name": "Email",
                "value": "email",
                "type": "text",
            },
            {
                "name": "Địa chỉ",
                "value": "address",
                "type": "text",
            },
            {
                "name": "Ngày lập",
                "value": "createAt",
                "type": "text",
            },
            {
                "name": "Tổng tiền",
                "value": "totalMoney",
                "type": "text",
            },
            {
                "name": "Trạng thái",
                "value": "status",
                "type": "select",
                "select": [
                    {
                        "name": "--- Chọn giá trị ---",
                        "value": "default",
                    },
                    {
                        "name": "Hoạt động",
                        "value": "1",
                    },
                    {
                        "name": "Ngừng Hoạt động",
                        "value": "0",
                    },
                ],
            }
        ]
        dataFilter = [
            {"name": "Tên khách hàng",
             "value": "name"},
            {"name": "Ngày lập",
             "value": "createAt"},
            {"name": "Tổng tiền",
             "value": "totalMoney"},

        ]
        data = GetListOrderAdminSerializers(data=request.data)
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
            data_orm = Order.objects.filter(
                q).order_by(field_order_by)[start:end]
        else:
            data_orm = Order.objects.filter(q)[start:end]
        count = Order.objects.filter(q).count()
        pageInfo = {"limit": limit, "page": page, "count": count}
        data = GetOrderSerializer(data_orm, many=True)
        index = page * limit + 1
        for item in data.data:
            item["stt"] = index
            index += 1
        return Response({"status": 200, "columns": columns, "rows": data.data, "pageInfo": pageInfo, "dataSearch": dataSearch, "dataFilter": dataFilter})

    def delete(self, request):
        ids_json = request.GET.get('ids')
        ids = json.loads(ids_json)
        if ids and len(ids) > 0:
            Order.objects.filter(id__in=tuple(ids)).delete()
            return Response({"status": 200, "messenger": "Xóa thành công"})
        return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"})
