import cv2
import dlib
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

# Lista de opciones para departamentos y ciudades
departamentos_y_ciudades = {
    "Amazonas": ["Leticia", "Puerto Nariño"],
    "Antioquia": ["Medellín", "Envigado", "Itagüí", "Sabaneta", "Rionegro"],
    "Arauca": ["Arauca", "Saravena"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Sabanalarga", "Galapa"],
    "Bolívar": ["Cartagena", "Turbaco"],
    "Boyacá": ["Tunja", "Duitama"],
    "Caldas": ["Manizales", "Villamaría"],
    "Caquetá": ["Florencia", "Morelia"],
    "Casanare": ["Yopal", "Tauramena"],
    "Cauca": ["Popayán", "Santander de Quilichao"],
    "Cesar": ["Valledupar", "La Jagua de Ibirico"],
    "Chocó": ["Quibdó", "Bajo Baudó"],
    "Córdoba": ["Montería", "Lorica"],
    "Cundinamarca": ["Bogotá", "Soacha", "Chía", "Zipaquirá", "Cajicá"],
    "Guainía": ["Inírida", "San Felipe"],
    "Guaviare": ["San José del Guaviare", "Calamar"],
    "Huila": ["Neiva", "Pitalito"],
    "La Guajira": ["Riohacha", "Maicao"],
    "Magdalena": ["Santa Marta", "Ciénaga"],
    "Meta": ["Villavicencio", "Acacías"],
    "Nariño": ["Pasto", "Tumaco"],
    "Norte de Santander": ["Cúcuta", "Villa de Rosario"],
    "Putumayo": ["Mocoa", "Villagarzón"],
    "Quindío": ["Armenia", "Salento"],
    "Risaralda": ["Pereira", "Dosquebradas"],
    "San Andrés y Providencia": ["San Andrés", "Providencia"],
    "Santander": ["Bucaramanga", "Floridablanca", "Girón", "Piedecuesta", "San Gil"],
    "Sucre": ["Sincelejo", "Corozal"],
    "Tolima": ["Ibagué", "Espinal"],
    "Valle del Cauca": ["Cali", "Buenaventura", "Tuluá", "Palmira", "Cartago"],
    "Vaupés": ["Mitú", "Carurú"],
    "Vichada": ["Puerto Carreño", "Cumaribo"]
}

# Opciones para localidades y drogas
opciones_localidad = [
    "Santa Fe", "Mártires", "Datos de prueba"
]

opciones_drogas = ["N/A","Alcohol", "Cigarrillo", "Marihuana", "Cocaína", "Heroína", "LSD", "Éxtasis", "Metanfetamina", "Bazuco"]

opciones_genero = ["Masculino", "Femenino"]

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

# Función para registrar un usuario
def registrar_usuario(common_id):
    def guardar_datos():
        nombre = nombre_entry.get().strip().lower()
        apellido = apellido_entry.get().strip().lower()
        departamento = departamento_var.get()
        ciudad = ciudad_var.get()
        fecha_nacimiento = fecha_nacimiento_entry.get_date()
        ano_situacion_calle = ano_situacion_calle_entry.get()
        edad_inicio_drogas = edad_inicio_drogas_entry.get()
        primera_droga = primera_droga_var.get()
        droga_frecuente_1 = droga_frecuente_1_var.get()
        droga_frecuente_2 = droga_frecuente_2_var.get()
        droga_frecuente_3 = droga_frecuente_3_var.get()
        localidad = localidad_var.get()
        ubicacion_frecuente = ubicacion_frecuente_entry.get()
        genero = genero_var.get()

        # Validación de campos vacíos
        if not all([nombre, apellido, departamento, ciudad, fecha_nacimiento, ano_situacion_calle, edad_inicio_drogas, primera_droga, droga_frecuente_1, droga_frecuente_2, droga_frecuente_3, localidad, ubicacion_frecuente, genero]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios. Por favor, llene todos los campos.")
            return
        
        # Validación lógica de fechas
        try:
            ano_situacion_calle_val = int(ano_situacion_calle)
            edad_inicio_drogas_val = int(edad_inicio_drogas)
        except ValueError:
            messagebox.showwarning("Advertencia", "Año de situación de calle y edad de inicio de drogas deben ser números enteros.")
            return

        hoy = datetime.now().date()
        
        # Calcular las fechas límites basadas en los años de situación de calle y inicio de drogas
        fecha_situacion_calle = datetime(ano_situacion_calle_val, 1, 1).date()
        fecha_inicio_drogas = datetime(fecha_nacimiento.year + edad_inicio_drogas_val, 1, 1).date()
        
        if not (fecha_nacimiento < fecha_situacion_calle):
            messagebox.showwarning("Advertencia", "La fecha de nacimiento debe ser anterior al año de situación de calle.")
            return

        if not (fecha_nacimiento < fecha_inicio_drogas):
            messagebox.showwarning("Advertencia", "La fecha de nacimiento debe ser anterior al año de inicio de drogas.")
            return

        user_data = {
            "nombre": nombre,
            "apellido": apellido,
            "departamento": departamento,
            "ciudad": ciudad,
            "fecha_nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
            "edad": calcular_edad(fecha_nacimiento.strftime("%d/%m/%Y")),
            "ano_situacion_calle": ano_situacion_calle,
            "tiempo_situacion_calle": calcular_anos_situacion_calle(ano_situacion_calle),
            "edad_inicio_drogas": edad_inicio_drogas,
            "primera_droga": primera_droga,
            "droga_frecuente_1": droga_frecuente_1,
            "droga_frecuente_2": droga_frecuente_2,
            "droga_frecuente_3": droga_frecuente_3,
            "localidad": localidad,
            "ubicacion_frecuente": ubicacion_frecuente,
            "genero": genero
        }

        # Asegúrate de que common_id esté correctamente definido
        if common_id is None:
            messagebox.showwarning("Advertencia", "ID del usuario no está definido.")
            return

        # Actualizar el registro en la base de datos
        users_collection.update_one({"_id": common_id}, {"$set": user_data}, upsert=True)
        dialogo.destroy()

    def actualizar_ciudades(*args):
        ciudad_var.set('')
        departamento = departamento_var.get()
        ciudades = departamentos_y_ciudades.get(departamento, [])
        ciudad_combobox['values'] = ciudades

    dialogo = tk.Tk()
    dialogo.title("Registrar Usuario")

    # Crear etiquetas y campos de entrada para los datos del usuario
    nombre_label = tk.Label(dialogo, text="Nombres")
    nombre_label.grid(row=0, column=0)
    nombre_entry = tk.Entry(dialogo)
    nombre_entry.grid(row=0, column=1)

    apellido_label = tk.Label(dialogo, text="Apellidos")
    apellido_label.grid(row=1, column=0)
    apellido_entry = tk.Entry(dialogo)
    apellido_entry.grid(row=1, column=1)

    departamento_label = tk.Label(dialogo, text="Departamento de nacimiento")
    departamento_label.grid(row=2, column=0)
    departamento_var = tk.StringVar(dialogo)
    departamento_combobox = ttk.Combobox(dialogo, textvariable=departamento_var, values=list(departamentos_y_ciudades.keys()))
    departamento_combobox.grid(row=2, column=1)
    departamento_combobox.bind("<<ComboboxSelected>>", actualizar_ciudades)

    ciudad_label = tk.Label(dialogo, text="Ciudad de nacimiiento")
    ciudad_label.grid(row=3, column=0)
    ciudad_var = tk.StringVar(dialogo)
    ciudad_combobox = ttk.Combobox(dialogo, textvariable=ciudad_var)
    ciudad_combobox.grid(row=3, column=1)

    fecha_nacimiento_label = tk.Label(dialogo, text="Fecha de nacimiento")
    fecha_nacimiento_label.grid(row=4, column=0)
    fecha_nacimiento_entry = DateEntry(dialogo, date_pattern='dd/MM/yyyy')
    fecha_nacimiento_entry.grid(row=4, column=1)

    ano_situacion_calle_label = tk.Label(dialogo, text="Año en que comenzo a habitar la Calle")
    ano_situacion_calle_label.grid(row=5, column=0)
    ano_situacion_calle_entry = tk.Entry(dialogo)
    ano_situacion_calle_entry.grid(row=5, column=1)

    edad_inicio_drogas_label = tk.Label(dialogo, text="Edad de Inicio en Drogas")
    edad_inicio_drogas_label.grid(row=6, column=0)
    edad_inicio_drogas_entry = tk.Entry(dialogo)
    edad_inicio_drogas_entry.grid(row=6, column=1)

    primera_droga_label = tk.Label(dialogo, text="Primera Droga Consumida")
    primera_droga_label.grid(row=7, column=0)
    primera_droga_var = tk.StringVar(dialogo)
    primera_droga_combobox = ttk.Combobox(dialogo, textvariable=primera_droga_var, values=opciones_drogas)
    primera_droga_combobox.grid(row=7, column=1)

    droga_frecuente_1_label = tk.Label(dialogo, text="Droga Frecuente 1")
    droga_frecuente_1_label.grid(row=8, column=0)
    droga_frecuente_1_var = tk.StringVar(dialogo)
    droga_frecuente_1_combobox = ttk.Combobox(dialogo, textvariable=droga_frecuente_1_var, values=opciones_drogas)
    droga_frecuente_1_combobox.grid(row=8, column=1)

    droga_frecuente_2_label = tk.Label(dialogo, text="Droga Frecuente 2")
    droga_frecuente_2_label.grid(row=9, column=0)
    droga_frecuente_2_var = tk.StringVar(dialogo)
    droga_frecuente_2_combobox = ttk.Combobox(dialogo, textvariable=droga_frecuente_2_var, values=opciones_drogas)
    droga_frecuente_2_combobox.grid(row=9, column=1)

    droga_frecuente_3_label = tk.Label(dialogo, text="Droga Frecuente 3")
    droga_frecuente_3_label.grid(row=10, column=0)
    droga_frecuente_3_var = tk.StringVar(dialogo)
    droga_frecuente_3_combobox = ttk.Combobox(dialogo, textvariable=droga_frecuente_3_var, values=opciones_drogas)
    droga_frecuente_3_combobox.grid(row=10, column=1)

    localidad_label = tk.Label(dialogo, text="Localidad")
    localidad_label.grid(row=11, column=0)
    localidad_var = tk.StringVar(dialogo)
    localidad_combobox = ttk.Combobox(dialogo, textvariable=localidad_var, values=opciones_localidad)
    localidad_combobox.grid(row=11, column=1)

    ubicacion_frecuente_label = tk.Label(dialogo, text="Ubicación Frecuente")
    ubicacion_frecuente_label.grid(row=12, column=0)
    ubicacion_frecuente_entry = tk.Entry(dialogo)
    ubicacion_frecuente_entry.grid(row=12, column=1)

    genero_label = tk.Label(dialogo, text="Género")
    genero_label.grid(row=13, column=0)
    genero_var = tk.StringVar(dialogo)
    genero_combobox = ttk.Combobox(dialogo, textvariable=genero_var, values=opciones_genero)
    genero_combobox.grid(row=13, column=1)

    guardar_button = tk.Button(dialogo, text="Guardar", command=guardar_datos)
    guardar_button.grid(row=14, columnspan=2)

    dialogo.mainloop()

# Función para capturar imagen y puntos faciales
def capturar_imagen_puntos_faciales(user_id):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar la imagen.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        caras = detector(gray)

        for cara in caras:
            shape = predictor(gray, cara)
            landmarks = [(p.x, p.y) for p in shape.parts()]
            for (x, y) in landmarks:
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

            cv2.imshow("Captura de Imagen", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    imagen_path = "captura_usuario.png"
    cv2.imwrite(imagen_path, frame)

    with open(imagen_path, "rb") as f:
        imagen_id = fs.put(f, filename=imagen_path)

    puntos_faciales = {'landmarks': landmarks}

    facial_data = {
        'user_id': user_id,
        'imagen_id': imagen_id,
        'puntos_faciales': puntos_faciales,
        'fecha': datetime.now()
    }

    facial_data_collection.insert_one(facial_data)

# Función principal
def main():
    common_id = ObjectId()
    registrar_usuario(common_id)
    capturar_imagen_puntos_faciales(common_id)

if __name__ == "__main__":
    main()