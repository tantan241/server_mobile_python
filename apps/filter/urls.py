
from django.urls import path
from .views import GetFilterView
urlpatterns = [
   
    path('get-filter', GetFilterView.as_view(), name="get-filter")
]