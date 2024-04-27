import cv2
from mtcnn import MTCNN
import os

# Función para detectar y guardar el rostro capturado
def detectar_guardar(frame, face_detector, output_dir):
    # Detectar rostros en el frame
    faces = face_detector.detect_faces(frame)
    
    # Si se detecta al menos un rostro
    if faces:
        # Tomar el primer rostro detectado
        face = faces[0]['box']
        x, y, width, height = face
        face_img = frame[y:y+height, x:x+width]
        
        # Crear la carpeta si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Guardar la imagen del rostro en la carpeta especificada
        cv2.imwrite(os.path.join(output_dir, 'captured_face.jpg'), face_img)
        print("Rostro capturado y guardado en:", output_dir)

# Inicializar el detector de rostros
face_detector = MTCNN()

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Crear una ventana para mostrar la captura de video
cv2.namedWindow("Face Capture", cv2.WINDOW_NORMAL)

while True:
    # Leer un frame del video
    ret, frame = cap.read()
    
    # Mostrar el frame en la ventana
    cv2.imshow("Face Capture", frame)
    
    # Detectar y guardar el rostro capturado
    detectar_guardar(frame, face_detector, 'rostros')
    
    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura de video y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()