from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
from datetime import datetime
# Create your models here.

class OrderMethod(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
class Order(models.Model):
    order_method = models.ForeignKey(OrderMethod,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    totalMoney = models.DecimalField(max_digits=15, decimal_places=2,default=0)
    createdAt =models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    number = models.IntegerField()