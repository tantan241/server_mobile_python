from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import Response
from rest_framework import status, generics, permissions
from .serializers import GetBrandAdminSerializers, AddProductAdminSerializer, GetListProductAdminSerializers, GetBrandSerializer, GetProductSerializer, ProductSerializer, GetRoleReviewProductSerializers, CompareProductSerializers, AddBrandSerializers, GetListProductAdminSerializers
from .models import Brand, Product
from apps.comment.models import Comment
from apps.user.models import CustomUser
from apps.order.models import OrderDetail, Order
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Sum
from math import *
import json
from datetime import datetime
import pytz
from apps.user.models import User
# Create your views here.


class GetBrand(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        dataRes = []
        try:
            data = Brand.objects.filter(status=1)
            for item in data:
                dataRes.append({
                    "name": item.name,
                    "id": item.id,
                })
            return Response({"data": dataRes, "status": 200, "messenger": "Lấy dữ liệu thành công."}, status=status.HTTP_200_OK)
        except:
            return Response({"messenger": "Lấy dữ liệu thất bại.", "status": 400}, status=status.HTTP_200_OK)


class GetMobile(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        dataRequest = GetProductSerializer(data=request.data)
        q = Q()
        if not dataRequest.is_valid():
            results = Product.objects.filter(status=1).all()
            data = ProductSerializer(results, many=True)
            return Response({"messenger": "Lỗi", "status": 400})
        filter = dataRequest.data["filter"]
        order_by = ""
        for key in filter:
            if key == "brand" and len(filter["brand"]) > 0:
                q |= Q(brand__in=filter[key])
            elif key == "ram" and len(filter["ram"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=[
                           {"value": f"{item}", "name": f"{key}"}])
            elif key == "rom" and len(filter["rom"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=[
                           {"value": f"{item}", "name": f"{key}"}])
                # q |= Q(rom__in=filter[key])
            elif key == "frontCamera" and len(filter["frontCamera"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=[
                           {"value": f"{item}", "name": f"{key}"}])
                # q |= Q(frontCamera__in=filter[key])
        for key in dataRequest.data:
            if key == "type":
                type = dataRequest.data["type"]
                if type == 0 or type == 1:
                    q &= Q(type=type)
            if key == "price":
                price = dataRequest.data["price"]
                if (price["fromPrice"] > 0 and price["toPrice"] > 0):
                    if (price["fromPrice"] > price["toPrice"]):
                        return Response({"messenger": "Từ giá không được lớn hơn đến giá", "status": 400})
                    else:
                        q &= Q(price__gt=price["fromPrice"])
                        q &= Q(price__lt=price["toPrice"])
            if key == "order":
                order = dataRequest.data["order"]
                if order == "asc":  # tăng dần
                    order_by = "asc"
                if order == "desc":
                    order_by = "desc"  # giảm dần
        page = dataRequest.data["page"]
        numberProduct = dataRequest.data["numberProduct"]
        start = (page-1) * numberProduct
        end = start + numberProduct
        if (order_by == "asc"):
            results = Product.objects.filter(
                q & Q(status=1)).order_by("price")[start:end]
        elif (order_by == "desc"):
            results = Product.objects.filter(
                q & Q(status=1)).order_by("-price")[start:end]
        else:
            results = Product.objects.filter(q & Q(status=1))[start:end]
        data = ProductSerializer(results, many=True)
        for item in data.data:
            res = self.get_rating_in_product(item["id"])
            for key in res:
                item[key] = res[key]
        count = results = Product.objects.filter(q & Q(status=1)).count()
        numberPage = ceil(count / numberProduct)
        return Response({"data": data.data,
                         "numberPage": numberPage,
                         "status": 200})

    def get(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        q = request.query_params.get('query', None)
        if id:
            try:
                results = Product.objects.get(id=id)
                data = ProductSerializer(results)
                return Response({"data": data.data, "status": 200})
            except:
                return Response("Không tồn tại sản phẩm")
        if q:
            results = Product.objects.filter(Q(name__icontains=q)).values()
            for item in results:
                res = self.get_rating_in_product(item["id"])
                for key in res:
                    item[key] = res[key]
            return Response({"status": 200, "data": results})

    def get_rating_in_product(self, id_model):
        res = Comment.objects.filter(product_id=id_model).aggregate(
            Avg("rating"))['rating__avg']
        num = Comment.objects.filter(product_id=id_model).exclude(
            rating__isnull=True).count()
        return {"rating": res,
                "number_rating": num
                }


class GetRoleReviewProductView(APIView):
    def post(self, request):
        data = GetRoleReviewProductSerializers(data=request.data)
        if not data.is_valid():
            return Response("Lỗi dữ liệu đầu vào", status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=data.data["userId"])
        product = Product.objects.get(id=data.data["productId"])
        commented = 0
        try:
            Comment.objects.get(user=user, product=product)
            commented = 1
        except:
            commented = 0
        return Response({"status": 200, "commented": commented
                         })


class GetTopBuyProductView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        limit = request.GET.get("limit")
        if not limit:
            return Response("Không tồn tại limit")
        order_details = OrderDetail.objects.values('product_id').annotate(
            sum=Sum('number')).order_by('-sum')[:int(limit)]
        list_product_id = list()
        for item in order_details:
            list_product_id.append(item["product_id"])
        products = Product.objects.filter(id__in=list_product_id)
        data = ProductSerializer(products, many=True)
        return Response({"status": 200, "data": data.data})


class GetListProductCompareView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        type = request.data.get('type')
        brand = request.data.get("brand")
        type_acc = request.data.get("typeAccessory")
        q = Q()
        if type:
            q &= Q(type=type)
        if brand:
            q &= Q(brand=brand)
        if type_acc:
            q &= Q(type_accessory=type_acc)
        products = Product.objects.filter(q)
        data = ProductSerializer(products, many=True)
        return Response({"status": 200, "data": data.data})


class CompareProductView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = CompareProductSerializers(data=request.data)
        if not data.is_valid():
            return Response({"status": 400}, status=status.HTTP_400_BAD_REQUEST)
        id_product_1 = data.data["productId1"]
        id_product_2 = data.data["productId2"]
        try:
            product_1 = Product.objects.get(id=id_product_1)
            data_product_1 = ProductSerializer(product_1)
            product_2 = Product.objects.get(id=id_product_2)
            data_product_2 = ProductSerializer(product_2)
            return Response({"status": 200, "product1": data_product_1.data, "product2": data_product_2.data})
        except:
            return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"}, status=status.HTTP_400_BAD_REQUEST)


# admin
class GetBrandAdminView(APIView):
    def post(self, request):
        fields = ["name", "status"]
        columns = [
            {"field": "stt", "headerName": "STT",
                "sortable": False,  "flex": 0.2, "filterable": False},
            {"field": "name", "headerName": "Tên Thương Hiệu", "sortable": False,
                "filterable": False, "flex": 1},
            {"field": "status", "headerName": "Trạng Thái",
                "filterable": False, "flex": 1, "sortable": False},
        ]
        dataSearch = [
            {
                "name": "--- Chọn giá trị ---",
                "value": "default",
                "type": "",
            },
            {
                "name": "Tên thương hiệu",
                "value": "name",
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
            {"name": "Tên thương hiệu",
             "value": "name"}

        ]
        data = GetBrandAdminSerializers(data=request.data)
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
            data_orm = Brand.objects.filter(
                q).order_by(field_order_by)[start:end]
        else:
            data_orm = Brand.objects.filter(q)[start:end]
        count = Brand.objects.filter(q).count()
        pageInfo = {"limit": limit, "page": page, "count": count}
        data = GetBrandSerializer(data_orm, many=True)
        index = page * limit + 1
        for item in data.data:
            item["stt"] = index
            index += 1
        return Response({"status": 200, "columns": columns, "rows": data.data, "pageInfo": pageInfo, "dataSearch": dataSearch, "dataFilter": dataFilter})

    def delete(self, request):
        ids_json = request.GET.get('ids')
        ids = json.loads(ids_json)
        if ids and len(ids) > 0:
            Brand.objects.filter(id__in=tuple(ids)).delete()
            return Response({"status": 200, "messenger": "Xóa thành công"})
        return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"})


class GetOneBrandView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        print(request.GET)
        if not id:
            return Response({"status": 400, "messenger": "Lỗi không tìm thấy id"}, status=status.HTTP_400_BAD_REQUEST)
        brand = Brand.objects.get(id=id)
        brand = GetBrandSerializer(brand)
        return Response({"status": 200, "data": brand.data})


class AddBrandView(APIView):
    def post(self, request):
        data = AddBrandSerializers(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dũ liệu đẩu vào"}, status=status.HTTP_400_BAD_REQUEST)
        name = data.data["name"].title()
        id = data.data.get("id")
        status = data.data["status"]
        if id:
            Brand.objects.filter(id=id).update(name=name, status=status)
            return Response({"status": 200, "messenger": "Cập nhâp thành công"})
        Brand.objects.create(name=name, status=status)
        return Response({"status": 200, "messenger": "Thêm mới thành công"})


class GetListProductAdminView(APIView):
    def post(self, request):
        fields = ["name", "price", "discount", "image",
                  "specifications", "type", "brand", "number", "status"]
        columns = [
            {"field": "stt", "headerName": "STT",
                "sortable": False,  "flex": 0.2, "filterable": False},
            {"field": "name", "headerName": "Tên Sản Phẩm",
                "filterable": False, "flex": 1.5, "sortable": False},
            {"field": "price", "headerName": "Giá",
             "filterable": False, "flex": 1, "sortable": False},
            {"field": "discount", "headerName": "Giảm Giá",
             "filterable": False, "flex": 0.5, "sortable": False},
            {"field": "number", "headerName": "Số Lượng",
             "filterable": False, "flex": 0.5, "sortable": False},
            {"field": "type", "headerName": "Loại sản phẩm",
             "filterable": False, "flex": 0.7, "sortable": False},
            {"field": "brand", "headerName": "Thương Hiệu",
             "filterable": False, "flex": 1, "sortable": False},
            {"field": "status", "headerName": "Trạng Thái",
                "filterable": False, "flex": 1, "sortable": False},
        ]
        brands = Brand.objects.all().values()
        brandSearch = list()
        brandSearch.append({
            "name": "--- Chọn giá trị ---",
            "value": "default",
        })
        for item in brands:
            brandSearch.append({"name": item["name"], "value": item["id"]})

        dataSearch = [
            {
                "name": "--- Chọn giá trị ---",
                "value": "default",
                "type": "",
            },
            {
                "name": "Tên Sản Phẩm",
                "value": "name",
                "type": "text",
            },
            {
                "name": "Giá",
                "value": "price",
                "type": "text",
            },
            {
                "name": "Giảm Giá",
                "value": "discount",
                "type": "text",
            },
            {
                "name": "Thông Số",
                "value": "specifications",
                "type": "text",
            },
            {
                "name": "Số Lượng",
                "value": "number",
                "type": "text",
            },
            {
                "name": "Thương Hiệu",
                "value": "brand",
                "type": "select",
                "select": brandSearch
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
            {"name": "Tên sản phẩm",
             "value": "name"},
            {"name": "Giá sản phẩm",
             "value": "price"},
            {"name": "Giảm giá",
             "value": "discount"},
            {"name": "Số lượng còn",
             "value": "number"},

        ]
        data = GetListProductAdminSerializers(data=request.data)
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
            data_orm = Product.objects.filter(
                q).order_by(field_order_by)[start:end]
        else:
            data_orm = Product.objects.filter(q)[start:end]
        count = Product.objects.filter(q).count()
        pageInfo = {"limit": limit, "page": page, "count": count}
        data = ProductSerializer(data_orm, many=True)
        index = page * limit + 1
        for item in data.data:
            item["stt"] = index
            index += 1
        return Response({"status": 200, "columns": columns, "rows": data.data, "pageInfo": pageInfo, "dataSearch": dataSearch, "dataFilter": dataFilter})

    def delete(self, request):
        ids_json = request.GET.get('ids')
        ids = json.loads(ids_json)
        if ids and len(ids) > 0:
            Product.objects.filter(id__in=tuple(ids)).delete()
            return Response({"status": 200, "messenger": "Xóa thành công"})
        return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"})


class GetAllBrandForProductView(APIView):
    def get(self, request):
        brand = Brand.objects.all().values()
        return Response({"status": 200, "data": brand})


class AddProductAdminView(APIView):
    def post(self, request):
        data = AddProductAdminSerializer(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dữ liệu đầu vào"}, status=status.HTTP_400_BAD_REQUEST)
        id = data.data.get("id")
        description = data.data.get(
            "description") if data.data.get("description") else ""
        name = data.data["name"]
        price = data.data["price"]
        discount = data.data["discount"]
        slug = data.data["slug"]
        image = data.data["image"]
        images = data.data["images"]
        number = data.data["number"]
        status = data.data["status"]
        type = data.data["type"]
        typeAccessory = data.data["typeAccessory"]
        brand = data.data["brand"]
        specifications = data.data["specifications"]
        brandO = Brand.objects.get(id=brand)
        print(data.data)
        if id:
            Product.objects.filter(id=id).update(status=status, name=name, type=type, type_accessory=typeAccessory, brand=brandO, specifications=specifications,
                                                 price=price, discount=discount, slug=slug, image=image, images=images, number=number, description=description)
            return Response({"status": 200, "messenger": "Cập nhập thành công"})
        Product.objects.create(status=status, name=name, type=type, type_accessory=typeAccessory, brand=brandO, specifications=specifications,
                               price=price, discount=discount, slug=slug, image=image, images=images, number=number, description=description)
        return Response({"status": 200, "messenger": "Thêm mới thành công"})


class GetOneProductView(APIView):
    def get(self, request):
        id = request.GET.get('id')
        print(request.GET)
        if not id:
            return Response({"status": 400, "messenger": "Lỗi không tìm thấy id"}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=id)
        product = ProductSerializer(product)
        return Response({"status": 200, "data": product.data})


class GetDashboardView(APIView):
    def convert_date(self, date):
        dt = datetime.strptime(date, '%d/%m/%Y')
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        iso_dt = dt.astimezone(tz).isoformat()
        return iso_dt

    def post(self, request):
        fromDate = self.convert_date(request.data["fromDate"])
        toDate = self.convert_date(request.data["toDate"])
        orders = Order.objects.filter(
            Q(createdAt__gte=fromDate) & Q(createdAt__lte=toDate))
        # Số hóa đơn lập
        order_count = orders.count()
        # Số user mới
        user_count = User.objects.filter(
            Q(date_joined__gte=fromDate) & Q(date_joined__lte=toDate)).count()
        # Sản phẩm bán chạy nhất
        order_details = OrderDetail.objects.values('product_id').annotate(
            sum=Sum('number')).order_by('-sum')[:1]
        product_id = order_details[0]["product_id"]
        product = Product.objects.get(id=product_id)
        product_name = product.name
        # Số sản phẩm hết hàng
        product_number_0 = Product.objects.filter(number=0).count()
        product_out_of_stock = Product.objects.filter(status =1,number=0).values()
        # Tổng số sản phẩm đã bán
        list_id_product = list()
        for order in orders: 
            list_id_product.append(order.id)
        order_details = OrderDetail.objects.filter(order_id__in= list_id_product)
        total_price = order_details.aggregate(Sum('price'))['price__sum']
        total_product = order_details.aggregate(Sum('number'))['number__sum']
        return Response({"status": 200, "data": {
            "order_count": order_count,
            "user_count": user_count,
            "product_name": product_name,
            "product_number_0": product_number_0,
            "total_price": total_price,
            "total_product": total_product,
            "product_out_of_stock": product_out_of_stock,
        }})