'''
#Borra informacion documento puntual
from pymongo import MongoClient

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")
db = client['ClusterSemillero']  # Usa el nombre correcto de la base de datos
users_collection = db['users']

# Eliminar todos los documentos de la colección 'fs.chunks'
result = users_collection.delete_many({})
print(f"{result.deleted_count} documentos eliminados.")

'''
#Borra toda la informacion de los documentos
from pymongo import MongoClient

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")
db = client['ClusterSemillero']  # Usa el nombre correcto de la base de datos

# Listado de colecciones a eliminar datos
collections = ['facial_data', 'fs.chunks', 'fs.files', 'photos', 'users']

# Eliminar todos los documentos de cada colección
for collection_name in collections:
    collection = db[collection_name]
    result = collection.delete_many({})
    print(f"{result.deleted_count} documentos eliminados de la colección {collection_name}.")
