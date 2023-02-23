from django.urls import path
from .views import SendCommentView
urlpatterns = [
    path("send-comment/",SendCommentView.as_view(),name="Sen-Comment")
]
