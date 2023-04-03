
from django.urls import path, include
from .views import CreateOrderView, CountOrderView, GetListOrder
urlpatterns = [

    path('create-order', CreateOrderView.as_view(), name='create-order'),
    path('count-order', CountOrderView.as_view(), name='count-order'),
    path('get-list-order', GetListOrder.as_view(), name='get-list-order'),
]
