from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics,permissions
from .models import Filter
from .serializers import GetFilterSerializer
from django.db.models import Q
# Create your views here.
class GetFilterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        type = request.GET["type"]
        q =Q()
        if type == "home":
             q = Q(value="brand")
        elif type == "mobile":
            q |= Q(value="ram")
            q |= Q(value="brand")
        elif type == "accessory":
            # q |= Q(value="ram")
            q |= Q(value="brand")
        filterModel = Filter.objects.filter(q).values()
        return Response(filterModel)