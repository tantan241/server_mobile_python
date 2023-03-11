from rest_framework import serializers
from .models import Filter

class GetFilterSerializer(serializers.Serializer):
    class Meta:
        model= Filter
        fields = '__all__'
