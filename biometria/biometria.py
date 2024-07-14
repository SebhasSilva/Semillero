import cv2
import os
import dlib
import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from pymongo import MongoClient
import gridfs
from bson import ObjectId

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")
db = client['ClusterSemillero']
users_collection = db['users']
facial_data_collection = db['facial_data']
photos_collection = db['photos']
fs = gridfs.GridFS(db)

# Lista de opciones para la localidad
opciones_localidad = [
    "Usaquén", "Chapinero", "Santa Fe", "San Cristóbal", "Usme",
    "Tunjuelito", "Bosa", "Kennedy", "Fontibón", "Engativá",
    "Suba", "Barrios Unidos", "Teusaquillo", "Mártires",
    "Antonio Nariño", "Puente Aranda", "Candelaria",
    "Rafael Uribe Uribe", "Ciudad Bolívar", "Sumapaz"
]

# Lista de opciones para las drogas
opciones_drogas = ["N/A", "Marihuana", "Cocaína", "Heroína", "LSD", "Éxtasis", "Metanfetamina", "Bazuco"]

# Función para calcular la edad actual
def calcular_edad(fecha_nacimiento):
    fecha_nac = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    hoy = datetime.now()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    return edad

# Función para calcular años en situación de calle
def calcular_anos_situacion_calle(ano_situacion_calle):
    hoy = datetime.now()
    anos_situacion_calle = hoy.year - int(ano_situacion_calle)
    return anos_situacion_calle

# Función para calcular años consumiendo drogas
def calcular_anos_consumiendo_drogas(ano_inicio_drogas):
    hoy = datetime.now()
    anos_consumo_drogas = hoy.year - int(ano_inicio_drogas)
    return anos_consumo_drogas

# Función para mostrar el formulario y registrar un usuario
def registrar_usuario(common_id):
    user_data = {}

    def guardar_datos():
        nombre = nombre_entry.get().lower()
        apellido = apellido_entry.get().lower()
        ciudad = ciudad_entry.get().lower()
        fecha_nacimiento = fecha_nacimiento_entry.get()
        ano_situacion_calle = ano_situacion_calle_entry.get()
        edad_inicio_drogas = edad_inicio_drogas_entry.get()
        primera_droga = primera_droga_var.get()
        droga_frecuente_1 = droga_frecuente_1_var.get()
        droga_frecuente_2 = droga_frecuente_2_var.get()
        droga_frecuente_3 = droga_frecuente_3_var.get()
        localidad = localidad_var.get()
        ubicacion_frecuente = ubicacion_frecuente_entry.get().lower()

        if nombre and apellido and ciudad and fecha_nacimiento and ano_situacion_calle and edad_inicio_drogas:
            user_data["_id"] = common_id
            user_data["Nombres"] = nombre
            user_data["Apellidos"] = apellido
            user_data["Fecha de Nacimiento"] = fecha_nacimiento
            user_data["Edad"] = calcular_edad(fecha_nacimiento)
            user_data["Ciudad_Nacimiento"] = ciudad
            user_data["Hace cuanto tiempo esta en situación de calle"] = ano_situacion_calle
            user_data["Años en situación de calle"] = calcular_anos_situacion_calle(ano_situacion_calle)
            user_data["Edad de inicio de drogas"] = edad_inicio_drogas
            user_data["Años consumiendo drogas"] = calcular_anos_consumiendo_drogas(str(datetime.now().year - int(edad_inicio_drogas)))
            user_data["Primera droga consumida"] = primera_droga
            user_data["Droga más frecuente"] = droga_frecuente_1
            user_data["Droga medianamente frecuente"] = droga_frecuente_2
            user_data["Droga menos frecuente"] = droga_frecuente_3
            user_data["Localidad"] = localidad
            user_data["Ubicación frecuente"] = ubicacion_frecuente
            dialogo.destroy()
            root.quit()
        else:
            messagebox.showwarning("Campos Incompletos", "Por favor complete todos los campos.")

    root = tk.Tk()
    root.withdraw()

    dialogo = tk.Toplevel(root)
    dialogo.title("Registro de Usuario")

    tk.Label(dialogo, text="Ingrese sus datos personales").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    tk.Label(dialogo, text="Nombres:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    nombre_entry = ttk.Entry(dialogo)
    nombre_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Apellidos:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    apellido_entry = ttk.Entry(dialogo)
    apellido_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Ciudad de Nacimiento:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    ciudad_entry = ttk.Entry(dialogo)
    ciudad_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Fecha de Nacimiento (dd/mm/yyyy):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    fecha_nacimiento_entry = DateEntry(dialogo, date_pattern="dd/mm/yyyy")
    fecha_nacimiento_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Año en que empezó situación de calle:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    ano_situacion_calle_entry = ttk.Entry(dialogo)
    ano_situacion_calle_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Edad de inicio de consumo de drogas:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    edad_inicio_drogas_entry = ttk.Entry(dialogo)
    edad_inicio_drogas_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Primera droga consumida:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    primera_droga_var = tk.StringVar(dialogo)
    primera_droga_var.set(opciones_drogas[0])
    primera_droga_menu = ttk.OptionMenu(dialogo, primera_droga_var, *opciones_drogas)
    primera_droga_menu.grid(row=7, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Droga más frecuente:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
    droga_frecuente_1_var = tk.StringVar(dialogo)
    droga_frecuente_1_var.set(opciones_drogas[0])
    droga_frecuente_1_menu = ttk.OptionMenu(dialogo, droga_frecuente_1_var, *opciones_drogas)
    droga_frecuente_1_menu.grid(row=8, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Droga medianamente frecuente:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
    droga_frecuente_2_var = tk.StringVar(dialogo)
    droga_frecuente_2_var.set(opciones_drogas[0])
    droga_frecuente_2_menu = ttk.OptionMenu(dialogo, droga_frecuente_2_var, *opciones_drogas)
    droga_frecuente_2_menu.grid(row=9, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Droga menos frecuente:").grid(row=10, column=0, sticky="e", padx=5, pady=5)
    droga_frecuente_3_var = tk.StringVar(dialogo)
    droga_frecuente_3_var.set(opciones_drogas[0])
    droga_frecuente_3_menu = ttk.OptionMenu(dialogo, droga_frecuente_3_var, *opciones_drogas)
    droga_frecuente_3_menu.grid(row=10, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Localidad:").grid(row=11, column=0, sticky="e", padx=5, pady=5)
    localidad_var = tk.StringVar(dialogo)
    localidad_var.set(opciones_localidad[0])
    localidad_menu = ttk.OptionMenu(dialogo, localidad_var, *opciones_localidad)
    localidad_menu.grid(row=11, column=1, padx=5, pady=5)

    tk.Label(dialogo, text="Ubicación frecuente:").grid(row=12, column=0, sticky="e", padx=5, pady=5)
    ubicacion_frecuente_entry = ttk.Entry(dialogo)
    ubicacion_frecuente_entry.grid(row=12, column=1, padx=5, pady=5)

    ttk.Button(dialogo, text="Guardar", command=guardar_datos).grid(row=13, column=0, columnspan=2, pady=10)

    root.mainloop()
    return user_data

# Función para capturar foto y almacenar datos
def capturar_foto_y_almacenar_datos(user_data, common_id):
    # Capturar la imagen de la cámara
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo acceder a la cámara.")
            break
        cv2.imshow('Captura de foto - Presione Espacio para tomar la foto', frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

    img_path = f"{common_id}_foto.jpg"
    cv2.imwrite(img_path, frame)

    with open(img_path, 'rb') as f:
        img_data = f.read()

    # Subir la imagen a GridFS usando el mismo ID
    img_id = fs.put(img_data, filename=img_path, _id=common_id)

    # Guardar la foto en la colección 'photos'
    photo_data = {
        "_id": common_id,
        "image_id": img_id,
        "filename": img_path,
        "uploaded_at": datetime.now()
    }
    
    try:
        photos_collection.insert_one(photo_data)
    except Exception as e:
        print(f"Error al insertar foto: {e}")

    # Detectar puntos faciales usando dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    landmarks = []
    for rect in rects:
        shape = predictor(gray, rect)
        landmarks = [(p.x, p.y) for p in shape.parts()]

    # Guardar los datos en las colecciones correspondientes
    facial_data = {
        "_id": common_id,
        "id_usuario": str(common_id),
        "id_foto": img_id,
        "landmarks": landmarks
    }

    # Intentar insertar datos en facial_data_collection
    try:
        facial_data_collection.insert_one(facial_data)
    except Exception as e:
        print(f"Error al insertar datos faciales: {e}")

    # Insertar datos del usuario en la colección 'users'
    try:
        users_collection.insert_one(user_data)
    except Exception as e:
        print(f"Error al insertar datos de usuario: {e}")

    # Eliminar la imagen temporal
    os.remove(img_path)

if __name__ == "__main__":
    common_id = ObjectId()
    user_data = registrar_usuario(common_id)
    if user_data:
        capturar_foto_y_almacenar_datos(user_data, common_id)
        print("Datos del usuario y foto almacenados exitosamente.")