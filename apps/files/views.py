from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import FilesSerializer
from .models import File
import datetime
import os
from apps.user.models import CustomUser
# Create your views here.

class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        f = request.FILES.get('file')   
        now = datetime.datetime.now()
        str_date =str(int(now.timestamp()))
        if not f:
            return Response({"status": 400,
                             "message": "Không tìm thấy file"})
        file_name = f"{str_date}{f.name}"
        file_path = os.path.join('media',file_name )
        with open(file_path, 'wb') as file:
                for chunk in f.chunks():
                    file.write(chunk)
        return Response({"status": 200,
                         "fileName": file_name})