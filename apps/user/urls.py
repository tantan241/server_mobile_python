from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Demo,CreateUser,LoginView
urlpatterns = [
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('user/',Demo.as_view(),name="demo"),
   path('create-user/',CreateUser.as_view(),name="create-user"),
   path('login/',LoginView.as_view(),name="login")
]
