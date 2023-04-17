from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import SendCommentSerializer, GetCommentSerializer, GetListCommentAdminSerializers,UpdateCommentAdminSerializer
from .models import Comment
from apps.user.models import CustomUser
from django.db.models import Q
import json
from apps.product.models import Product

# Create your views here.


class SendCommentView(generics.ListAPIView):
    def post(self, request):
        data = SendCommentSerializer(data=request.data)
        print(request.data)
        if not data.is_valid():
            return Response({"Messenger": "Lỗi dữ liệu đầu vào", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        user = data.data["user"]
        product = data.data["product"]
        rating = data.data["rating"]
        content = ""
        image = ""
        for key in data.data:
            if key == 'content':
                content = data.data[key]
            if key == 'image':
                image = data.data[key]
        checkComment = Comment.objects.filter(user_id=user, product_id=product)
        print(checkComment)
        if len(checkComment) > 0:
            return Response({"messenger": "Cập nhập thành công", "status": 200})
        Comment.objects.create(user_id=user, product_id=product,
                               content=content, rating=rating, image=image)
        return Response({"messenger": "Đánh giá  thành công", "status": 200, "data": {"user": user, "product": product, "content": content, "rating": rating, "image": image}}, status=status.HTTP_200_OK)


class GetCommentById(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        id = request.GET["id"]
        commentQuery = Comment.objects.filter(product_id=id)
        totalComment = commentQuery.count()
        star_1 = commentQuery.filter(rating=1).count()
        star_2 = commentQuery.filter(rating=2).count()
        star_3 = commentQuery.filter(rating=3).count()
        star_4 = commentQuery.filter(rating=4).count()
        star_5 = commentQuery.filter(rating=5).count()
        comments = []
        for item in commentQuery:
            data = dict()
            user = CustomUser.objects.get(id=item.user_id)
            data['id'] = item.id
            data["name_user"] = user.fullName
            data["star"] = item.rating
            data["image"] = item.image
            data["content"] = item.content
            comments.append(data)
        return Response({"total": totalComment, "star": {
            "star_1": star_1,
            "star_2": star_2,
            "star_3": star_3,
            "star_4": star_4,
            "star_5": star_5
        },
            "comments": comments})


# admin
class GetListCommentAdminView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['id']
        try:
            product = Product.objects.get(id=int(product_id))
        except:
            return Response("Không tồn tại sản phẩm")
        fields = ["content", "rating", "image", "createdAt",
                  "user_id",  "status"]
        columns = [
            {
                "field": "stt",
                "headerName": "STT",
                "sortable": False,
                "flex": 0.2,
                "filterable": False
            },
            {
                "field": "content",
                "headerName": "Nội Dung",
                "filterable": False,
                "flex": 3,
                "sortable": False
            },
            {
                "field": "rating",
                "headerName": "Sao",
                "filterable": False,
                "flex": 0.2,
                "sortable": False
            },
            {
                "field": "image",
                "headerName": "Ảnh",
                "filterable": False,
                "flex": 0.5,
                "sortable": False,
            },
            {
                "field": "createdAt",
                "headerName": "Ngày viết",
                "filterable": False,
                "flex": 0.7,
                "sortable": False
            },
            {
                "field": "user",
                "headerName": "Người viết",
                "filterable": False,
                "flex": 0.7,
                "sortable": False
            },
            {
                "field": "status",
                "headerName": "Trạng Thái",
                "filterable": False,
                "flex": 0.9,
                "sortable": False
            }
        ]

        dataSearch = [
            {
                "name": "--- Chọn giá trị ---",
                "value": "default",
                "type": "",
            },
            {
                "name": "Nội Dung",
                "value": "content",
                "type": "text",
            },
            {
                "name": "Số Sao",
                "value": "rating",
                "type": "text",
            },
            {
                "name": "Ngày Viết",
                "value": "user",
                "type": "text",
            },
            # {
            #     "name": "Người Viết",
            #     "value": "brand",
            #     "type": "select",
            #     "select": brandSearch
            # },
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
            {"name": "Số Sao",
             "value": "rating"},

        ]
        data = GetListCommentAdminSerializers(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dữ liệu đầu vào"}, status=status.HTTP_400_BAD_REQUEST)
        limit = data.data["limit"]
        page = data.data["page"]
        search = data.data["search"]
        sort = data.data.get("sort")

        q = Q()
        q &= Q(id__gte=0)
        q &= Q(product=product)

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
            data_orm = Comment.objects.filter(
                q).order_by(field_order_by)[start:end]
        else:
            data_orm = Comment.objects.filter(q)[start:end]
        count = Comment.objects.filter(q).count()
        pageInfo = {"limit": limit, "page": page, "count": count}
        data = GetCommentSerializer(data_orm, many=True)
        index = page * limit + 1
        for item in data.data:
            item["stt"] = index
            user = CustomUser.objects.get(id=item["user"])
            user = user.fullName
            item["user"] = user
        return Response({"status": 200, "columns": columns, "rows": data.data, "pageInfo": pageInfo, "dataSearch": dataSearch, "dataFilter": dataFilter})

    def delete(self, request):
        ids_json = request.GET.get('ids')
        ids = json.loads(ids_json)
        if ids and len(ids) > 0:
            Comment.objects.filter(id__in=tuple(ids)).delete()
            return Response({"status": 200, "messenger": "Xóa thành công"})
        return Response({"status": 400, "messenger": "Không tồn tại sản phẩm"})


class GetOneCommentView(APIView):
    def get(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({"status": 400, "messenger": "Lỗi không tìm thấy id"}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.get(id=id)
        comment = GetCommentSerializer(comment)
        return Response({"status": 200, "data": comment.data})

class UpdateCommentView(APIView):
    def post(self, request):
        data = UpdateCommentAdminSerializer(data=request.data)
        if not data.is_valid():
            return Response({"status": 400, "messenger": "Lỗi dữ liệu đầu vào"}, status=status.HTTP_400_BAD_REQUEST)
        id = data.data.get("id")
        status = data.data["status"]
        Comment.objects.filter(id=id).update(status=status)
        return Response({"status": 200, "messenger": "Cập nhập thành công"})
       