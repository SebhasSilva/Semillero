import sys
import os
import django
import pymongo
import numpy as np
import json
from django.conf import settings
from bson.objectid import ObjectId

# Configuración de Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aplicacionweb.settings')
django.setup()

from photos.models import FacialLandmarks

# Conectar a MongoDB usando PyMongo
try:
    mongo_client = pymongo.MongoClient(settings.MONGO_URI)
    mongo_db = mongo_client['ClusterSemillero']
    mongo_collection = mongo_db['facial_data']
    
    # Crear un índice en los puntos faciales para mejorar la búsqueda
    mongo_collection.create_index([("facial_points", pymongo.ASCENDING)])
except Exception as e:
    print(f"Error al conectar con MongoDB: {e}")
    sys.exit(1)

# Algoritmo de comparación de puntos faciales
def compare_landmarks(landmarks1, landmarks2):
    try:
        landmarks1 = np.array(landmarks1)
        landmarks2 = np.array(landmarks2)
        if landmarks1.shape != landmarks2.shape:
            print(f"Las formas de los puntos faciales no coinciden: {landmarks1.shape} vs {landmarks2.shape}")
            return np.inf
        distance = np.linalg.norm(landmarks1 - landmarks2)
        return distance
    except Exception as e:
        print(f"Error al comparar puntos faciales: {e}")
        return np.inf

# Constantes
DISTANCE_THRESHOLD = 7000  # Ajusta este valor según tus necesidades

def process_landmarks():
    try:
        print("Obteniendo puntos faciales desde Django...")
        django_landmarks = FacialLandmarks.objects.all()
        total_landmarks = django_landmarks.count()
        print(f"Total de puntos faciales obtenidos desde Django: {total_landmarks}")

        # Obtener todos los puntos faciales de MongoDB
        mongo_landmarks = list(mongo_collection.find({"facial_points": {"$exists": True}}))
        print(f"Total de puntos faciales obtenidos desde MongoDB: {len(mongo_landmarks)}")

        for django_landmark in django_landmarks:
            print(f"\nComparando puntos faciales para Django ID {django_landmark.id}...")
            django_data = json.loads(django_landmark.data)
            django_points = django_data.get('landmarks', [])

            distances = []

            for mongo_landmark in mongo_landmarks:
                mongo_points = mongo_landmark.get('facial_points', [])
                if mongo_points:
                    distance = compare_landmarks(django_points, mongo_points)
                    if distance <= DISTANCE_THRESHOLD:
                        distances.append((distance, mongo_landmark['_id']))

            # Ordenar distancias y obtener las tres coincidencias más cercanas
            distances.sort(key=lambda x: x[0])
            top_matches = distances[:3]

            if top_matches:
                print("Coincidencias más cercanas:")
                for i, match in enumerate(top_matches, 1):
                    print(f"{i}. Mongo ID {match[1]}, Distancia: {match[0]:.2f}")
            else:
                print("No se encontraron coincidencias cercanas para este punto facial.")

    except Exception as e:
        print(f"Error al procesar puntos faciales: {e}")
        import traceback
        traceback.print_exc()

# Función principal
def main():
    try:
        process_landmarks()
    except Exception as e:
        print(f"Error en la ejecución principal: {e}")
    finally:
        if 'mongo_client' in locals():
            mongo_client.close()

if __name__ == "__main__":
    main()