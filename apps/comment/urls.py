from django.urls import path
from .views import SendCommentView,GetCommentById
urlpatterns = [
    path("send-comment",SendCommentView.as_view(),name="Send-Comment"),
    path("get-comment",GetCommentById.as_view(),name="Get-Comment")

]
