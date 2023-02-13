from django.urls import path

from .views import GetBrand,GetMobile
urlpatterns = [
    path("get-brand/", GetBrand.as_view(), name="get-brand"),
    path("get-products/", GetMobile.as_view(), name="get-mobile")
]
