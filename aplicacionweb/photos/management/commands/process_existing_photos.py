import cv2
import dlib
import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from photos.models import Photo, FacialLandmarks
from django.db import IntegrityError

# Inicializa el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()

# Especifica la ruta completa del archivo shape_predictor_68_face_landmarks.dat
predictor_path = r"C:\Users\silva\OneDrive\Documentos\Proyectoteinco\aplicacionweb\photos\shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

def process_facial_landmarks(photo):
    """
    Procesa los puntos faciales de una foto y los guarda en la base de datos.
    """
    image_path = photo.image.path

    # Lee la imagen
    image = cv2.imread(image_path)

    # Convierte la imagen en escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detecta rostros en la imagen
    faces = detector(gray)

    if len(faces) > 0:
        landmarks_data = []
        for i, face in enumerate(faces):
            # Encuentra los puntos faciales
            landmarks = predictor(gray, face)

            # Crear un diccionario con los datos de la captura
            data = {
                "timestamp": str(datetime.now()),
                "landmarks": [(landmarks.part(j).x, landmarks.part(j).y) for j in range(68)]
            }
            landmarks_data.append(data)

            # Dibuja los puntos faciales en la imagen (opcional, para visualización)
            for j in range(68):
                x, y = landmarks.part(j).x, landmarks.part(j).y
                cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

        # Guarda o actualiza los datos en el modelo FacialLandmarks
        try:
            facial_landmarks, created = FacialLandmarks.objects.update_or_create(
                photo=photo,
                defaults={'data': json.dumps(landmarks_data)}
            )
            if created:
                print(f"Created new FacialLandmarks for {photo.image.name}")
            else:
                print(f"Updated existing FacialLandmarks for {photo.image.name}")
        except IntegrityError as e:
            print(f"Error processing {photo.image.name}: {str(e)}")

    # Opcional: guarda la imagen con los puntos faciales dibujados
    output_image_path = os.path.join('processed_images', os.path.basename(image_path))
    os.makedirs('processed_images', exist_ok=True)
    cv2.imwrite(output_image_path, image)

class Command(BaseCommand):
    help = 'Process existing photos and save facial landmarks'

    def handle(self, *args, **kwargs):
        photos = Photo.objects.all()
        for photo in photos:
            process_facial_landmarks(photo)
            self.stdout.write(self.style.SUCCESS(f'Processed {photo.image.name}'))