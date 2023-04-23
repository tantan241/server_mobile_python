from django.urls import path
from .views import SendCommentView, GetCommentById, GetListCommentAdminView, GetOneCommentView, UpdateCommentView, GetInfoCommentAdminView
urlpatterns = [
    path("send-comment", SendCommentView.as_view(), name="Send-Comment"),
    path("get-comment", GetCommentById.as_view(), name="Get-Comment"),
    path("admin/<id>/list-comment", GetListCommentAdminView.as_view(),
         name="admin-get-list-Comment"),
    path("admin/get-one-comment", GetOneCommentView.as_view(),
         name="admin-get-one-comment"),
    path("admin/update-comment", UpdateCommentView.as_view(),
         name="admin-update-comment"),

    path("admin/<id>/get-info-comment", GetInfoCommentAdminView.as_view(),
         name="admin-get-info-comment"),

]
