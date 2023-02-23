from rest_framework import serializers
from .models import Comment

class SendCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields = ("user","product","content","rating")
class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Comment
        fields = "__all__"