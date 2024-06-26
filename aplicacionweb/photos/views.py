from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView
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

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = 'users/photo_confirm_delete.html'  # Asegúrate de que la ruta sea correcta
    success_url = reverse_lazy('profile')  # Redirige al perfil del usuario después de eliminar

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.visible = False  # Marca la foto como no visible
        self.object.save()
        return redirect(self.success_url)

    def get_queryset(self):
        """
        Limita la eliminación a las fotos del usuario actual.
        """
        return self.model.objects.filter(user=self.request.user)