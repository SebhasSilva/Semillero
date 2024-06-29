from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Photo, FacialLandmarks
from .serializers import PhotoSerializer

import cv2
import dlib
import json
import os
from datetime import datetime

# Inicializa el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()

# Especifica la ruta completa del archivo shape_predictor_68_face_landmarks.dat
predictor_path = r"C:\Users\silva\OneDrive\Documentos\Proyectoteinco\aplicacionweb\photos\shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

class PhotoUploadView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        photo = serializer.save(user=self.request.user)
        process_facial_landmarks(photo)

class PhotoListView(ListView):
    model = Photo
    template_name = 'users/photo_list.html'  # Ruta actualizada a la plantilla en users/templates/users/
    context_object_name = 'photos'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)

@login_required
def upload_photos(request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photos')
        photo_urls = []

        for photo in photos:
            photo_instance = Photo.objects.create(user=request.user, image=photo)
            process_facial_landmarks(photo_instance)
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

def process_facial_landmarks(photo):
    """
    Procesa los puntos faciales de una foto y los guarda en la base de datos.
    """
    image_path = photo.image.path

    # Lee la imagen
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error al leer la imagen en la ruta: {image_path}")
        return

    # Convierte la imagen en escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detecta rostros en la imagen
    faces = detector(gray)
    print(f"Rostros detectados: {len(faces)}")

    if len(faces) > 0:
        for i, face in enumerate(faces):
            # Encuentra los puntos faciales
            landmarks = predictor(gray, face)

            # Crear un diccionario con los datos de la captura
            data = {
                "timestamp": str(datetime.now()),
                "landmarks": [(landmarks.part(j).x, landmarks.part(j).y) for j in range(68)]
            }
            print(f"Datos de puntos faciales para la foto {photo.id}: {data}")

            # Guarda los datos en el modelo FacialLandmarks
            FacialLandmarks.objects.create(photo=photo, data=json.dumps(data))

            # Dibuja los puntos faciales en la imagen (opcional, para visualización)
            for j in range(68):
                x, y = landmarks.part(j).x, landmarks.part(j).y
                cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

    # Opcional: guarda la imagen con los puntos faciales dibujados
    output_image_path = os.path.join('processed_images', os.path.basename(image_path))
    os.makedirs('processed_images', exist_ok=True)
    cv2.imwrite(output_image_path, image)