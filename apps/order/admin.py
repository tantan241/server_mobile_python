from django.contrib import admin
from .models import Order,OrderDetail,OrderMethod
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(OrderMethod)