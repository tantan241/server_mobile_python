from rest_framework import serializers
from .models import File

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'