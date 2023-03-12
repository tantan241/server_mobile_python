from django.urls import path

from .views import GetBrand,GetMobile
urlpatterns = [
    path("get-brand", GetBrand.as_view(), name="get-brand"),
    path("get-product", GetMobile.as_view(), name="get-product")
]
