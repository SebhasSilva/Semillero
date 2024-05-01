import cv2
import os
import dlib
import json

# Obtener la ruta al directorio actual
dir_path = os.path.dirname(os.path.realpath(__file__))

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
                rostro_data[f'punto_{j+1}'] = (punto.x, punto.y)

            # Guardar la información del rostro en un archivo JSON
            with open(f'ROSTROS/rostro_{i+1}.json', 'w') as file:
                json.dump(rostro_data, file, indent=4)

            # Guardar la imagen del rostro
            rostro_img = frame[rostro.top():rostro.bottom(), rostro.left():rostro.right()]
            cv2.imwrite(f'ROSTROS/rostro_{i+1}.jpg', rostro_img)

            # Mostrar la imagen del rostro con puntos faciales
            for punto in puntos_faciales.parts():
                cv2.circle(rostro_img, (punto.x, punto.y), 2, (0, 255, 0), -1)

        # Mostrar la imagen en la ventana
        cv2.imshow('Capturando Rostro', frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cerrar la cámara y la aplicación
    cap.release()
    cv2.destroyAllWindows()

# Llamar a la función para capturar el rostro
capturar_rostro()