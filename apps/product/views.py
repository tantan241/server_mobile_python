from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import Response
from rest_framework import status, generics, permissions
from .serializers import GetBrandSerializer, GetProductSerializer, GetProductDetailsSerializer
from .models import Brand, Product,ProductVariant
from django.db.models import Q
# Create your views here.


class GetBrand(APIView):
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
            results = ProductVariant.objects.select_related(
                'product').filter(product__status=1).all()
            data = GetProductDetailsSerializer(results, many=True)
            return Response({"messenger":"Lỗi", "status": 400})
        filter = dataRequest.data["filter"]
        for key in filter:
            if key == "brand" and len(filter["brand"]) > 0:
                q |= Q(product__brand__in=filter[key])
            elif key == "ram" and len(filter["ram"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=f"ram={item}")
            elif key == "rom" and len(filter["rom"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=f"rom={item}")
                # q |= Q(rom__in=filter[key])
            elif key == "frontCamera" and len(filter["frontCamera"]) > 0:
                for item in filter[key]:
                    q |= Q(specifications__contains=f"frontCamera={item}")
                # q |= Q(frontCamera__in=filter[key])
        for key in dataRequest.data:
            if key == "type":
                type = dataRequest.data["type"]
                if type == 0 or type == 1:
                    q &= Q(product__type=type)
            if key == "price":
                price = dataRequest.data["price"]
                if (price["fromPrice"] > 0 and price["toPrice"] > 0):
                    if (price["fromPrice"] > price["toPrice"]):
                        return Response({"messenger": "Từ giá không được lớn hơn đến giá", "status": 400})
                    else:
                        q &= Q(product__price__gt=price["fromPrice"])
                        q &= Q(product__price__lt=price["toPrice"])
        print(q)
        results = ProductVariant.objects.select_related(
            'product').filter(q & Q(product__status=1))
        data = GetProductDetailsSerializer(results, many=True)
        return Response({"data": data.data,
                         "status": 200})
