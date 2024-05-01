import cv2
import os
import dlib
import json
import random
from tkinter import *

# Obtener la ruta al directorio actual
dir_path = os.path.dirname(os.path.realpath(__file__))

# Cargar el detector de rostros de dlib
detector_rostros = dlib.get_frontal_face_detector()
predictor_puntos_faciales = dlib.shape_predictor(os.path.join(dir_path, "shape_predictor_68_face_landmarks.dat"))

# Crear la carpeta "ROSTROS" si no existe
if not os.path.exists('ROSTROS'):
    os.makedirs('ROSTROS')

# Función para capturar el rostro y sus puntos faciales
def capturar_rostro(nombre, apellido, edad, ciudad_nacimiento):
    # Activar la cámara
    cap = cv2.VideoCapture(0)

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

            # Guardar información de los puntos faciales en un diccionario
            rostro_data = {}
            for j, punto in enumerate(puntos_faciales.parts()):
                rostro_data[f'punto_{j+1}'] = [punto.x, punto.y]

            # Generar ID de usuario
            id_usuario = str(random.randint(100000, 999999))

            # Verificar si el usuario ya está registrado
            base_de_datos = cargar_base_de_datos()
            if id_usuario in base_de_datos:
                print("Usuario ya registrado con ID:", id_usuario)
                return

            # Guardar la información del usuario en la base de datos
            base_de_datos[id_usuario] = {
                "ID": id_usuario,
                "Nombre": nombre,
                "Apellido": apellido,
                "Edad": edad,
                "Ciudad_Nacimiento": ciudad_nacimiento,
                "Rostro": f"rostro_{id_usuario}.jpg"
            }

            # Guardar la base de datos actualizada
            guardar_base_de_datos(base_de_datos)

            # Guardar la información del rostro en un archivo JSON
            with open(f'ROSTROS/rostro_{id_usuario}.json', 'w') as file:
                json.dump(rostro_data, file, indent=4)

            # Guardar la imagen del rostro
            rostro_img = frame[rostro.top():rostro.bottom(), rostro.left():rostro.right()]
            cv2.imwrite(f'ROSTROS/rostro_{id_usuario}.jpg', rostro_img)

            # Mostrar la imagen del rostro con puntos faciales
            for punto in puntos_faciales.parts():
                cv2.circle(rostro_img, (punto.x, punto.y), 2, (0, 255, 0), -1)

            # Mostrar mensaje de usuario registrado
            print("Usuario registrado con ID:", id_usuario)

            # Cerrar la cámara y la aplicación
            cap.release()
            cv2.destroyAllWindows()
            return id_usuario

        # Mostrar la imagen en la ventana
        cv2.imshow('Capturando Rostro', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Función para cargar la base de datos desde el archivo JSON
def cargar_base_de_datos():
    base_de_datos_path = os.path.join(dir_path, "base_de_datos.json")
    if not os.path.exists(base_de_datos_path):
        return {}
    with open(base_de_datos_path, 'r') as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError:
            return {}

# Función para guardar la base de datos en el archivo JSON
def guardar_base_de_datos(base_de_datos):
    base_de_datos_path = os.path.join(dir_path, "base_de_datos.json")
    with open(base_de_datos_path, 'w') as file:
        json.dump(base_de_datos, file, indent=4)

# Función para mostrar el formulario y capturar la información del usuario
def registrar_usuario():
    # Crear ventana principal
    ventana = Tk()
    ventana.title("Registro de Usuario")
    ventana.geometry("300x200")

    # Variables para almacenar la información del usuario
    nombre = StringVar()
    apellido = StringVar()
    edad = IntVar()
    ciudad_nacimiento = StringVar()

    # Etiquetas y cuadros de texto del formulario
    etiqueta_nombre = Label(ventana, text="Nombre:")
    etiqueta_nombre.grid(row=0, column=0)
    cuadro_nombre = Entry(ventana, textvariable=nombre)
    cuadro_nombre.grid(row=0, column=1)

    etiqueta_apellido = Label(ventana, text="Apellido:")
    etiqueta_apellido.grid(row=1, column=0)
    cuadro_apellido = Entry(ventana, textvariable=apellido)
    cuadro_apellido.grid(row=1, column=1)

    etiqueta_edad = Label(ventana, text="Edad:")
    etiqueta_edad.grid(row=2, column=0)
    cuadro_edad = Entry(ventana, textvariable=edad)
    cuadro_edad.grid(row=2, column=1)

    etiqueta_ciudad = Label(ventana, text="Ciudad de Nacimiento:")
    etiqueta_ciudad.grid(row=3, column=0)
    cuadro_ciudad = Entry(ventana, textvariable=ciudad_nacimiento)
    cuadro_ciudad.grid(row=3, column=1)

    # Función para capturar el rostro y la información del usuario
    def capturar():
        nombre_usuario = nombre.get()
        apellido_usuario = apellido.get()
        edad_usuario = edad.get()
        ciudad_usuario = ciudad_nacimiento.get()
        id_usuario = capturar_rostro(nombre_usuario, apellido_usuario, edad_usuario, ciudad_usuario)

        if id_usuario:
            mensaje_usuario_registrado = Label(ventana, text="Usuario registrado con ID: " + id_usuario)
            mensaje_usuario_registrado.grid(row=5, columnspan=2)
            ventana.after(3000, ventana.destroy)

    # Botón para capturar el rostro y la información del usuario
    boton_capturar = Button(ventana, text="Capturar", command=capturar)
    boton_capturar.grid(row=4, columnspan=2)

    # Ejecutar la ventana
    ventana.mainloop()

# Ejecutar el registro de usuario
registrar_usuario()