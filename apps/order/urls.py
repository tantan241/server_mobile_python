
from django.urls import path, include
from .views import CreateOrderView,AddOrderAdmin, CountOrderView, GetListOrder, GetOrderDetail, GetListOrderAdminView, GetOneOrderView
urlpatterns = [

    path('create-order', CreateOrderView.as_view(), name='create-order'),
    path('count-order', CountOrderView.as_view(), name='count-order'),
    path('get-order-detail', GetOrderDetail.as_view(), name='get-order-detail'),
    path('get-list-order', GetListOrder.as_view(), name='get-list-order'),
    path("admin/list-order", GetListOrderAdminView.as_view(),
         name="admin-get-list-order"),
    path("admin/get-one-order", GetOneOrderView.as_view(),
         name="admin-get-one-order"),
      path("admin/add-order", AddOrderAdmin.as_view(),
         name="admin-add-order"),
]
