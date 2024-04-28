import cv2
import os
import dlib
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window


class RostrosApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        layout = BoxLayout(orientation='vertical')

        self.detector_rostros = dlib.get_frontal_face_detector()
        self.predictor_puntos_faciales = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.cap = cv2.VideoCapture(0)
        self.btn_capture = Button(text="Capturar Rostro")
        self.btn_capture.bind(on_press=self.capturar_rostro)

        layout.add_widget(self.btn_capture)
        return layout

    def capturar_rostro(self, instance):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostros en la imagen
        rostros = self.detector_rostros(gray)

        # Procesar cada rostro encontrado
        for i, rostro in enumerate(rostros):
            # Obtener puntos faciales del rostro
            puntos_faciales = self.predictor_puntos_faciales(gray, rostro)

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

        self.btn_capture.text = "Rostro Capturado"


if __name__ == '__main__':
    if not os.path.exists('ROSTROS'):
        os.makedirs('ROSTROS')

    RostrosApp().run()