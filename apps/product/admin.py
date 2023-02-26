from django.contrib import admin
from .models import Brand,Product,ProductDetail,ProductVariant
# Register your models here.
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductVariant)