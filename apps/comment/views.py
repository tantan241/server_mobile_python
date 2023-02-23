from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import SendCommentSerializer, GetCommentSerializer
from .models import Comment
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
