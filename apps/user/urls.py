from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Demo, CreateUser, LoginView, LoginAdmin, GetCustomerAdminView, GetOneCustomerView, AddCustomerView
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', Demo.as_view(), name="demo"),
    path('create-user', CreateUser.as_view(), name="create-user"),
    path('login', LoginView.as_view(), name="login"),
    path('api/admin/login', LoginAdmin.as_view(), name="admin-login"),
    path("api/user/admin/list-customer",
         GetCustomerAdminView.as_view(), name="admin-list-customer"),
    path("api/user/admin/get-one-customer",
         GetOneCustomerView.as_view(), name="admin-get-one-customer"),
    path("api/user/admin/add-customer", AddCustomerView.as_view(),
         name="admin-add-customer"),
]
