from django.db import models
from django.db import models
# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=150,default="")
    status = models.IntegerField(default=1)
    def __str__(self) :
        return str(self.name)
# class Product(models.Model):
#     name = models.CharField(max_length=155,default="")
    # slug = models.CharField(max_length=255,default="")
    # price = models.FloatField(default=0)
    # discount = models.IntegerField(default=0)
    # type = models.IntegerField(default=0)
    # image = models.CharField(max_length=255,default="")
    # status=models.IntegerField(default=1)
    # brand =models.ForeignKey(Brand,on_delete=models.CASCADE)
    # def __str__(self) :
    #     return self.name
# class ProductDetail(models.Model):
#     display = models.CharField(max_length=255,null=True,blank=True,default="")
#     system = models.CharField(max_length=255,null=True,blank=True,default="")
#     frontCamera = models.CharField(max_length=255,null=True,blank=True,default="")
#     rearCamera = models.CharField(max_length=255,null=True,blank=True,default="")
#     chip = models.CharField(max_length=255,null=True,blank=True,default="")
#     ram = models.CharField(max_length=255,null=True,blank=True,default="")
#     rom = models.CharField(max_length=255,null=True,blank=True,default="")
#     sim = models.CharField(max_length=255,null=True,blank=True,default="")
#     battery = models.CharField(max_length=255,null=True,blank=True,default="")
#     image = models.CharField(max_length=255,null=True,blank=True,default="")
#     typeProduct = models.IntegerField(default=1)
#     product = models.OneToOneField(Product,on_delete=models.CASCADE)

class Product(models.Model):
    # product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=155,default="")
    type = models.IntegerField(default=0)
    status=models.IntegerField(default=1)
    brand =models.ForeignKey(Brand,on_delete=models.CASCADE)
    slug = models.CharField(max_length=255,default="")
    price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    image = models.CharField(max_length=255)
    images= models.TextField(max_length=1000)
    number = models.IntegerField(default="0")
    specifications= models.JSONField()
    def __str__(self) :
        return str(f"{self.name}-{self.id}")
