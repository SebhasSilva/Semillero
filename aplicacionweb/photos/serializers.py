from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id', 'user', 'image', 'uploaded_at')
