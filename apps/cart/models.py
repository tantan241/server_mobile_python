from django.db import models
from apps.user.models import User
from apps.product.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
class CartDetail(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    price = models.FloatField(default=0)
