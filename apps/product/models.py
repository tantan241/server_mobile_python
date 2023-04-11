from django.db import models
from django.db import models
# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=150, default="")
    status = models.IntegerField(default=1)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    # product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=155, default="")
    type = models.IntegerField(default=0)
    type_accessory = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, default="")
    price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    image = models.CharField(max_length=255)
    images = models.TextField(max_length=1000)
    number = models.IntegerField(default="0")
    specifications = models.JSONField()

    def __str__(self):
        return str(f"{self.name}-{self.id}")
