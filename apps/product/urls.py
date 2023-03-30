from django.urls import path

from .views import GetBrand, GetMobile, GetRoleReviewProductView, GetTopBuyProductView, GetListProductCompareView, CompareProductView
urlpatterns = [
    path("get-brand", GetBrand.as_view(), name="get-brand"),
    path("get-product", GetMobile.as_view(), name="get-product"),
    path("get-list-product-compare", GetListProductCompareView.as_view(),
         name="get-list-product-compare"),
    path("get-top-product", GetTopBuyProductView.as_view(), name="get-top-product"),
    path("get-role-comment", GetRoleReviewProductView.as_view(),
         name="get-role-comment"),
    path("compare-product", CompareProductView.as_view(), name="compare-product"),
]
