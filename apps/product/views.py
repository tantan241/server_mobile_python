from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import Response
from rest_framework import status, generics, permissions
from .serializers import GetBrandSerializer, GetProductSerializer, ProductSerializer, GetRoleReviewProductSerializers, CompareProductSerializers
from .models import Brand, Product
from apps.comment.models import Comment
from apps.user.models import CustomUser
from apps.order.models import OrderDetail
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Sum
from math import *
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
        print(q)
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
