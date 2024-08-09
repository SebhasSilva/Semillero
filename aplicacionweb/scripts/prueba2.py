import sys
import os
import django

# Agrega la ruta del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configura el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplicacionweb.settings')

# Inicializa Django
django.setup()

# Importaciones después de la configuración de Django
from photos.models import FacialLandmarks
import pymongo
import numpy as np
from django.conf import settings

# Conectar a MongoDB usando PyMongo
mongo_client = pymongo.MongoClient(settings.MONGO_URI)
mongo_db = mongo_client[settings.MONGO_DB_NAME]
mongo_collection = mongo_db['facial_data']

# Algoritmo de comparación de puntos faciales
def compare_landmarks(landmarks1, landmarks2):
    landmarks1 = np.array(landmarks1)
    landmarks2 = np.array(landmarks2)
    if landmarks1.shape != landmarks2.shape:
        print(f"Las formas de los puntos faciales no coinciden: {landmarks1.shape} vs {landmarks2.shape}")
        return np.inf  # Devolver una gran distancia si no coinciden
    distance = np.linalg.norm(landmarks1 - landmarks2)
    return distance

# Obtener todos los puntos faciales desde Django
print("Obteniendo puntos faciales desde Django...")
django_landmarks = FacialLandmarks.objects.all()
print(f"Total de puntos faciales obtenidos desde Django: {django_landmarks.count()}")

for landmark in django_landmarks:
    # Obtener puntos faciales desde MongoDB
    print(f"\nComparando puntos faciales para Django ID {landmark.id}...")
    print(f"Puntos faciales desde Django: {landmark.data}")

    mongo_landmarks = mongo_collection.find()
    
    distances = []

    for mongo_landmark in mongo_landmarks:
        print(f"Puntos faciales desde MongoDB: {mongo_landmark['facial_points']}")
        distance = compare_landmarks(landmark.data['landmarks'], mongo_landmark['facial_points'])
        print(f"Distancia calculada: {distance}")
        distances.append((distance, mongo_landmark['_id']))
    
    # Ordenar distancias y obtener las tres coincidencias más cercanas
    distances.sort(key=lambda x: x[0])
    top_matches = distances[:3]

    for match in top_matches:
        print(f"Posible coincidencia: Mongo ID {match[1]}, Distancia: {match[0]}")

    if not distances:
        print("No se encontraron coincidencias cercanas para este punto facial.")
