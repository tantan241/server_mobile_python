from django.urls import path
from .views import AddCartView,GetCartView,UpdateNumberView,DeleteCartDetailView,DeleteCartView
urlpatterns = [
   path("add-cart",AddCartView.as_view(),name="add-cart"),
   path("get-cart",GetCartView.as_view(),name="get-cart"),
   path("update-cart",UpdateNumberView.as_view(),name="update-cart"),
   path("delete-cart",DeleteCartDetailView.as_view(),name="delete-cart"), #xóa từng sản phẩm
   path("delete-all-cart",DeleteCartView.as_view(),name="delete-cart"), #xóa hết 1 lượt
]