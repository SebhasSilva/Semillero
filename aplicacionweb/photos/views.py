from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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

@login_required
def upload_photos(request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photos')
        photo_urls = []

        for photo in photos:
            photo_instance = Photo.objects.create(user=request.user, image=photo)
            photo_urls.append({
                'url': photo_instance.image.url
            })

        return JsonResponse({'success': True, 'photos': photo_urls})

    return JsonResponse({'success': False})
