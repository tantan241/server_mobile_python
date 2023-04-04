
from django.urls import path, include
from .views import CreateOrderView, CountOrderView, GetListOrder,GetOrderDetail
urlpatterns = [

    path('create-order', CreateOrderView.as_view(), name='create-order'),
    path('count-order', CountOrderView.as_view(), name='count-order'),
    path('get-order-detail', GetOrderDetail.as_view(), name='get-order-detail'),
    path('get-list-order', GetListOrder.as_view(), name='get-list-order'),
]
