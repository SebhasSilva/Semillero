import uuid
from pymongo import MongoClient
from django.conf import settings
import math

client = MongoClient(settings.MONGODB_URI)
db = client['ClusterSemillero']
users_collection = db['users']
facial_data_collection = db['facial_data']

def generate_common_id():
    return str(uuid.uuid4())

def sync_with_mongodb(street_person):
    user_data = {
        "nombre": street_person.first_name,
        "apellido": street_person.last_name,
        "ciudad": street_person.birth_city,
        "genero": street_person.gender,
        "common_id": street_person.common_id,
        "fecha_nacimiento": street_person.birth_date.strftime("%d/%m/%Y") if street_person.birth_date else None,
        "alias": street_person.alias,
    }
    
    users_collection.update_one(
        {"common_id": street_person.common_id},
        {"$set": user_data},
        upsert=True
    )

def get_facial_data(common_id):
    return facial_data_collection.find_one({"common_id": common_id})

def compare_facial_data(facial_data1, facial_data2):
    if len(facial_data1) != len(facial_data2):
        return 0
    
    total_distance = 0
    for p1, p2 in zip(facial_data1, facial_data2):
        distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        total_distance += distance
    
    max_distance = math.sqrt(2) * 100 * len(facial_data1)  # Asumiendo coordenadas máximas de 100x100
    similarity = 1 - (total_distance / max_distance)
    return similarity

def calculate_overall_similarity(street_person, mongo_data):
    facial_similarity = compare_facial_data(
        get_facial_data(street_person.common_id)['facial_points'],
        get_facial_data(mongo_data['common_id'])['facial_points']
    )
    
    name_similarity = (
        compare_strings(street_person.first_name, mongo_data['nombre']) +
        compare_strings(street_person.last_name, mongo_data['apellido'])
    ) / 2
    
    city_similarity = compare_strings(street_person.birth_city, mongo_data['ciudad'])
    gender_similarity = 1 if street_person.gender == mongo_data['genero'] else 0
    
    overall_similarity = (
        0.4 * facial_similarity +
        0.3 * name_similarity +
        0.2 * city_similarity +
        0.1 * gender_similarity
    )
    
    return overall_similarity

def compare_strings(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    distance = levenshtein_distance(str1, str2)
    max_length = max(len(str1), len(str2))
    return 1 - (distance / max_length)

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]