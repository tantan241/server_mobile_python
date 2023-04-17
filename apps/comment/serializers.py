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

#admin 
class GetListCommentAdminSerializers(serializers.Serializer):
    limit = serializers.IntegerField(required=True)
    page = serializers.IntegerField(required=True)
    search = serializers.DictField(required=False)
    sort = serializers.DictField(required=False)

class UpdateCommentAdminSerializer(serializers.Serializer):   
    id = serializers.IntegerField(required=False)
    status = serializers.IntegerField(required=True)
    