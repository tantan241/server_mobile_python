from rest_framework import serializers
from .models import Comment

class SendCommentSerializer(serializers.ModelSerializer):
    image = serializers.CharField(allow_blank=True)
    class Meta:
        model= Comment
        fields = ("user","product","content","rating","image")
class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Comment
        fields = "__all__"