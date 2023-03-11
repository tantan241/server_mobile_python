from django.db import models
from apps.user.models import CustomUser
from apps.product.models import Product
import os
# Create your models here.
class Comment(models.Model):
    def get_path():
        pass
    content = models.TextField(max_length=1000, default='')
    rating = models.IntegerField(default=1)
    image = models.CharField(max_length=255, default="")
    status = models.IntegerField(default=1)
    createdAt =models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    image = models.CharField( max_length=254)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)