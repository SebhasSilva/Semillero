from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Photo
from .serializers import PhotoSerializer

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
