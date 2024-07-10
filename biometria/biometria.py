import cv2
import os
import dlib
import random
import string
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from pymongo import MongoClient

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")  # Reemplaza con tu URI de conexión
db = client['ClusterSemillero']  # Usa el nombre correcto de la base de datos
users_collection = db['users']
facial_data_collection = db['facial_data']
photos_collection = db['photos']

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
def registrar_usuario():
    user_data = {}

    def guardar_datos():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        ciudad = ciudad_entry.get()
        fecha_nacimiento = fecha_nacimiento_entry.get()
        ano_situacion_calle = ano_situacion_calle_entry.get()
        edad_inicio_drogas = edad_inicio_drogas_entry.get()
        primera_droga = primera_droga_var.get()
        droga_frecuente_1 = droga_frecuente_1_var.get()
        droga_frecuente_2 = droga_frecuente_2_var.get()
        droga_frecuente_3 = droga_frecuente_3_var.get()
        localidad = localidad_var.get()
        ubicacion_frecuente = ubicacion_frecuente_entry.get()

        if nombre and apellido and ciudad and fecha_nacimiento and ano_situacion_calle and edad_inicio_drogas:
            user_data["_id"] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
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

    tk.Label(dialogo, text="Ingrese sus datos personales").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    tk.Label(dialogo, text="Localidad:").grid(row=1, column=0, padx=10, pady=5)
    localidad_var = tk.StringVar(dialogo)
    localidad_var.set(opciones_localidad[0])
    localidad_dropdown = tk.OptionMenu(dialogo, localidad_var, *opciones_localidad)
    localidad_dropdown.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Ubicación frecuente:").grid(row=2, column=0, padx=10, pady=5)
    ubicacion_frecuente_entry = tk.Entry(dialogo)
    ubicacion_frecuente_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Nombre:").grid(row=3, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(dialogo)
    nombre_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Apellido:").grid(row=4, column=0, padx=10, pady=5)
    apellido_entry = tk.Entry(dialogo)
    apellido_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Fecha de Nacimiento:").grid(row=5, column=0, padx=10, pady=5)
    fecha_nacimiento_entry = tk.Entry(dialogo)
    fecha_nacimiento_entry.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Ciudad de Nacimiento:").grid(row=6, column=0, padx=10, pady=5)
    ciudad_entry = tk.Entry(dialogo)
    ciudad_entry.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Hace cuanto tiempo esta en situación de calle (Año):").grid(row=7, column=0, padx=10, pady=5)
    ano_situacion_calle_entry = tk.Entry(dialogo)
    ano_situacion_calle_entry.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="¿A qué edad comenzó a consumir drogas?:").grid(row=8, column=0, padx=10, pady=5)
    edad_inicio_drogas_entry = tk.Entry(dialogo)
    edad_inicio_drogas_entry.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Primera droga consumida:").grid(row=9, column=0, padx=10, pady=5)
    primera_droga_var = tk.StringVar(dialogo)
    primera_droga_var.set(opciones_drogas[0])
    primera_droga_dropdown = tk.OptionMenu(dialogo, primera_droga_var, *opciones_drogas)
    primera_droga_dropdown.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Droga más frecuente:").grid(row=10, column=0, padx=10, pady=5)
    droga_frecuente_1_var = tk.StringVar(dialogo)
    droga_frecuente_1_var.set(opciones_drogas[0])
    droga_frecuente_1_dropdown = tk.OptionMenu(dialogo, droga_frecuente_1_var, *opciones_drogas)
    droga_frecuente_1_dropdown.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Droga medianamente frecuente:").grid(row=11, column=0, padx=10, pady=5)
    droga_frecuente_2_var = tk.StringVar(dialogo)
    droga_frecuente_2_var.set(opciones_drogas[0])
    droga_frecuente_2_dropdown = tk.OptionMenu(dialogo, droga_frecuente_2_var, *opciones_drogas)
    droga_frecuente_2_dropdown.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(dialogo, text="Droga menos frecuente:").grid(row=12, column=0, padx=10, pady=5)
    droga_frecuente_3_var = tk.StringVar(dialogo)
    droga_frecuente_3_var.set(opciones_drogas[0])
    droga_frecuente_3_dropdown = tk.OptionMenu(dialogo, droga_frecuente_3_var, *opciones_drogas)
    droga_frecuente_3_dropdown.grid(row=12, column=1, padx=10, pady=5)

    tk.Button(dialogo, text="Guardar", command=guardar_datos).grid(row=13, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

    return user_data

# Función para detectar y guardar puntos faciales
def guardar_puntos_faciales(user_data):
    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame de la cámara.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            puntos_faciales = [(point.x, point.y) for point in landmarks.parts()]
            
            for idx, point in enumerate(puntos_faciales):
                pos = (point[0], point[1])
                cv2.circle(frame, pos, 2, (255, 0, 0), -1)
                cv2.putText(frame, str(idx), pos, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("Frame", frame)

            k = cv2.waitKey(1)
            if k == ord('s'):  # Cambié a 's' como indicaste
                filename = f"{user_data['_id']}.jpg"
                filepath = os.path.join("fotos", filename)
                cv2.imwrite(filepath, frame)
                print(f"Foto guardada en {filepath}")

                photo_data = {
                    "_id": user_data["_id"],  # Usamos el mismo ID para todas las colecciones
                    "user_id": user_data["_id"],
                    "filename": filename,
                    "filepath": filepath,
                    "timestamp": datetime.now().isoformat()
                }
                photos_collection.insert_one(photo_data)
                print("Datos de la foto guardados en MongoDB")

                facial_data = {
                    "_id": user_data["_id"],  # Usamos el mismo ID para todas las colecciones
                    "user_id": user_data["_id"],
                    "facial_points": puntos_faciales,
                    "timestamp": datetime.now().isoformat()
                }
                facial_data_collection.insert_one(facial_data)
                print("Datos de los puntos faciales guardados en MongoDB")

                cap.release()
                cv2.destroyAllWindows()
                return puntos_faciales, filename

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None, None

# Función principal
def main():
    user_data = registrar_usuario()
    if user_data:
        users_collection.insert_one(user_data)
        puntos_faciales, filename = guardar_puntos_faciales(user_data)
        if puntos_faciales and filename:
            print("Datos guardados exitosamente.")
        else:
            print("No se pudieron guardar los puntos faciales o la foto.")
    else:
        print("No se pudieron registrar los datos del usuario.")

if __name__ == "__main__":
    main()