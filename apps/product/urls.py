from django.urls import path

from .views import GetBrand, GetAllBrandForProductView, GetListProductAdminView, GetMobile, GetRoleReviewProductView, GetTopBuyProductView, GetListProductCompareView, CompareProductView, GetBrandAdminView, GetOneBrandView, AddBrandView
urlpatterns = [
    path("get-brand", GetBrand.as_view(), name="get-brand"),
    path("get-product", GetMobile.as_view(), name="get-product"),
    path("get-list-product-compare", GetListProductCompareView.as_view(),
         name="get-list-product-compare"),
    path("get-top-product", GetTopBuyProductView.as_view(), name="get-top-product"),
    path("get-role-comment", GetRoleReviewProductView.as_view(),
         name="get-role-comment"),
    path("compare-product", CompareProductView.as_view(), name="compare-product"),
    path("admin/list-brand", GetBrandAdminView.as_view(), name="admin-list-brand"),
    path("admin/get-one-brand", GetOneBrandView.as_view(),
         name="admin-get-one-brand"),
    path("admin/add-brand", AddBrandView.as_view(),
         name="admin-add-brand"),
    path("admin/list-product", GetListProductAdminView.as_view(),
         name="admin-get-list-brand"),
    path("admin/get-all-brand-product", GetAllBrandForProductView.as_view(),
         name="admin-get-all-brand-product"),

]
