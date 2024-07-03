import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure

# Cadena de conexión usando SRV
uri = "mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority"

try:
    # Crea el cliente MongoDB
    client = pymongo.MongoClient(uri)
    
    # Verifica la conexión al servidor
    client.admin.command('ping')
    print("Conectado exitosamente a MongoDB Atlas")

    # Accede a una base de datos y una colección
    db = client.get_database('ClusterSemillero')  # Asegúrate de que este es el nombre correcto de tu base de datos
    collection = db.get_collection('Usuarios')    # Asegúrate de que este es el nombre correcto de tu colección

    # Ahora puedes realizar operaciones en la colección, por ejemplo:
    documents = collection.find({})

    for doc in documents:
        print(doc)

except ConnectionFailure as e:
    print(f"No se pudo conectar a MongoDB Atlas: {e}")

except OperationFailure as e:
    print(f"Error en la operación: {e}")

finally:
    # Cierra la conexión al finalizar
    if 'client' in locals():
        client.close()
        print("Conexión a MongoDB cerrada")