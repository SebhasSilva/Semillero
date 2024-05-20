import cv2
import os
import dlib
import json
import random
import string
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Obtener la ruta al directorio actual
dir_path = os.path.dirname(os.path.realpath(__file__))
base_de_datos_file = os.path.join(dir_path, "base_de_datos.json")

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

# Función para cargar la base de datos
def cargar_base_de_datos():
    if os.path.exists(base_de_datos_file):
        with open(base_de_datos_file, 'r') as file:
            return json.load(file)
    else:
        return {}

# Función para guardar la base de datos
def guardar_base_de_datos(base_de_datos):
    with open(base_de_datos_file, 'w') as file:
        json.dump(base_de_datos, file, indent=4)

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
        ano_inicio_drogas = ano_inicio_drogas_entry.get()
        primera_droga = primera_droga_var.get()
        droga_frecuente_1 = droga_frecuente_1_var.get()
        droga_frecuente_2 = droga_frecuente_2_var.get()
        droga_frecuente_3 = droga_frecuente_3_var.get()
        localidad = localidad_var.get()
        ubicacion_frecuente = ubicacion_frecuente_entry.get()

        if nombre and apellido and ciudad and fecha_nacimiento and ano_situacion_calle and ano_inicio_drogas and localidad and ubicacion_frecuente:
            user_data["Nombres"] = nombre
            user_data["Apellidos"] = apellido
            user_data["Fecha de Nacimiento"] = fecha_nacimiento
            user_data["Edad"] = calcular_edad(fecha_nacimiento)
            user_data["Ciudad_Nacimiento"] = ciudad
            user_data["Hace cuanto tiempo esta en situación de calle"] = ano_situacion_calle
            user_data["Años en situación de calle"] = calcular_anos_situacion_calle(ano_situacion_calle)
            user_data["En qué año comenzó a consumir drogas"] = ano_inicio_drogas
            user_data["Años consumiendo drogas"] = calcular_anos_consumiendo_drogas(ano_inicio_drogas)
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

    tk.Label(dialogo, text="En qué año comenzó a consumir drogas:").grid(row=8, column=0, padx=10, pady=5)
    ano_inicio_drogas_entry = tk.Entry(dialogo)
    ano_inicio_drogas_entry.grid(row=8, column=1, padx=10, pady=5)

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

    return user_data if user_data else None

# Función para capturar el rostro y sus puntos faciales
def capturar_rostro():
    # Activar la cámara
    cap = cv2.VideoCapture(0)

    # Cargar el detector de rostros de dlib
    detector_rostros = dlib.get_frontal_face_detector()
    predictor_puntos_faciales = dlib.shape_predictor(os.path.join(dir_path, "shape_predictor_68_face_landmarks.dat"))

    # Crear la carpeta "ROSTROS" si no existe
    if not os.path.exists('ROSTROS'):
        os.makedirs('ROSTROS')

    # Cargar o crear la base de datos
    base_de_datos = cargar_base_de_datos()

    # Capturar el rostro y sus puntos faciales
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        rostros = detector_rostros(gray)

        # Procesar cada rostro encontrado
        for i, rostro in enumerate(rostros):
            # Obtener puntos faciales del rostro
            puntos_faciales = predictor_puntos_faciales(gray, rostro)

            # Generar un ID de usuario aleatorio
            id_usuario = ''.join(random.choices(string.digits, k=6))

            # Solicitar información al usuario
            info_usuario = registrar_usuario()

            if info_usuario is None:
                print("El usuario canceló el registro o no completó los datos.")
                # Si el usuario cancela, salimos del programa
                return

            print("Información del usuario obtenida:", info_usuario)

            # Guardar la información del formulario en la base de datos
            info_usuario["ID"] = id_usuario
            info_usuario["Rostro"] = f'rostro_{id_usuario}.jpg'
            base_de_datos[id_usuario] = info_usuario
            guardar_base_de_datos(base_de_datos)

            # Guardar información de los puntos faciales en un diccionario
            rostro_data = {}
            for j, punto in enumerate(puntos_faciales.parts()):
                rostro_data[f'punto_{j+1}'] = (punto.x, punto.y)

            # Guardar la información del rostro en un archivo JSON
            with open(f'ROSTROS/rostro_{id_usuario}.json', 'w') as file:
                json.dump(rostro_data, file, indent=4)

            # Definir un margen para ampliar la región del rostro
            margen = 40

            # Asegúrate de no exceder los límites de la imagen
            top = max(0, rostro.top() - margen)
            bottom = min(frame.shape[0], rostro.bottom() + margen)
            left = max(0, rostro.left() - margen)
            right = min(frame.shape[1], rostro.right() + margen)

            # Guardar la imagen del rostro con el margen adicional
            rostro_img = frame[top:bottom, left:right]
            cv2.imwrite(f'ROSTROS/rostro_{id_usuario}.jpg', rostro_img)

            # Mostrar la imagen del rostro con puntos faciales
            for punto in puntos_faciales.parts():
                cv2.circle(rostro_img, (punto.x, punto.y), 2, (0, 255, 0), -1)

            # Mostrar la información del registro
            messagebox.showinfo("Información de Registro", 
                                f"ID de Usuario: {id_usuario}\n"
                                f"Nombres: {info_usuario['Nombres']}\n"
                                f"Apellidos: {info_usuario['Apellidos']}\n"
                                f"Edad: {info_usuario['Edad']}\n"
                                f"Fecha de Nacimiento: {info_usuario['Fecha de Nacimiento']}\n"
                                f"Ciudad de Nacimiento: {info_usuario['Ciudad_Nacimiento']}\n"
                                f"Hace cuanto tiempo está en situación de calle: {info_usuario['Hace cuanto tiempo esta en situación de calle']}\n"
                                f"Años en situación de calle: {info_usuario['Años en situación de calle']}\n"
                                f"Ubicación frecuente: {info_usuario['Ubicación frecuente']}")

            # Cerrar la cámara y la aplicación
            cap.release()
            cv2.destroyAllWindows()
            return

        # Mostrar la imagen en la ventana
        cv2.imshow('Capturando Rostro', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Llamar a la función para capturar el rostro
capturar_rostro()
