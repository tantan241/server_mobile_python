from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import SendCommentSerializer, GetCommentSerializer
from .models import Comment
from apps.user.models import CustomUser
# Create your views here.


class SendCommentView(generics.ListAPIView):
    def post(self, request):
        data = SendCommentSerializer(data=request.data)
        if not data.is_valid():
            return Response({"Messenger": "Lỗi dữ liệu đầu vào", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        user = data.data["user"]
        product = data.data["product"]
        rating = data.data["rating"]
        content = ""
        for key in data.data:
            if key == 'content':
                content = data.data[key]
        checkComment = Comment.objects.filter(user_id=user, product_id=product)
        print(checkComment)
        if len(checkComment) > 0:
            return Response({"messenger": "Cập nhập thành công", "status": 200})
        Comment.objects.create(user_id=user, product_id=product,
                               content=content, rating=rating)
        return Response({"messenger": "Đánh giá  thành công", "status": 200, "data": {"user": user, "product": product, "content": content, "rating": rating}}, status=status.HTTP_200_OK)


class GetCommentById(APIView):
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
            comments.append(data)
        return Response({"total": totalComment, "star": {
            "star_1": star_1,
            "star_2": star_2,
            "star_3": star_3,
            "star_4": star_4,
            "star_5": star_5
        },
            "comments": comments})
