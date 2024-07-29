import cv2
import dlib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from pymongo import MongoClient
import gridfs
import uuid

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")
db = client['ClusterSemillero']
users_collection = db['users']
facial_data_collection = db['facial_data']
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

opciones_localidad = [
    "Santa Fe", "Mártires", "Datos de prueba"
]

opciones_drogas = ["N/A", "Alcohol", "Cigarrillo", "Marihuana", "Cocaína", "Heroína", "LSD", "Éxtasis", "Metanfetamina", "Bazuco"]

opciones_genero = ["Masculino", "Femenino"]

def calcular_edad(fecha_nacimiento):
    fecha_nac = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
    hoy = datetime.now()
    edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    return edad

def calcular_anos_situacion_calle(ano_situacion_calle):
    hoy = datetime.now()
    anos_situacion_calle = hoy.year - int(ano_situacion_calle)
    return anos_situacion_calle

def calcular_anos_consumiendo_drogas(ano_inicio_drogas):
    hoy = datetime.now()
    anos_consumo_drogas = hoy.year - int(ano_inicio_drogas)
    return anos_consumo_drogas

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
        no_es_usuario_de_calle = no_es_usuario_de_calle_var.get()

        if not all([nombre, apellido, departamento, ciudad, fecha_nacimiento, ano_situacion_calle, edad_inicio_drogas, primera_droga, droga_frecuente_1, droga_frecuente_2, droga_frecuente_3, localidad, ubicacion_frecuente, genero]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios. Por favor, llene todos los campos.")
            return

        try:
            ano_situacion_calle_val = int(ano_situacion_calle)
            edad_inicio_drogas_val = int(edad_inicio_drogas)
        except ValueError:
            messagebox.showwarning("Advertencia", "Año de situación de calle y edad de inicio de drogas deben ser números enteros.")
            return

        hoy = datetime.now().date()
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
            "genero": genero,
            "no_es_usuario_de_calle": no_es_usuario_de_calle,
            "common_id": common_id
        }

        if common_id is None:
            messagebox.showwarning("Advertencia", "ID del usuario no está definido.")
            return

        users_collection.update_one({"common_id": common_id}, {"$set": user_data}, upsert=True)
        dialogo.destroy()
        ventana.destroy()

    def actualizar_ciudades(*args):
        departamento = departamento_var.get()
        ciudades = departamentos_y_ciudades.get(departamento, [])
        ciudad_combobox['values'] = ciudades
        if not ciudades:
            ciudad_var.set('')

    dialogo = tk.Toplevel()
    dialogo.title("Registro de Usuario")

    main_frame = ttk.Frame(dialogo, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(1, weight=1)

    fields = [
        ("Nombre", tk.StringVar(), None),
        ("Apellido", tk.StringVar(), None),
        ("Departamento", tk.StringVar(), actualizar_ciudades),
        ("Ciudad", tk.StringVar(), None),
        ("Fecha de Nacimiento", tk.StringVar(), None),
        ("Año de Situación de Calle", tk.StringVar(), None),
        ("Edad de Inicio de Consumo de Drogas", tk.StringVar(), None),
        ("Primera Droga Consumida", tk.StringVar(), None),
        ("Droga de Consumo Frecuente 1", tk.StringVar(), None),
        ("Droga de Consumo Frecuente 2", tk.StringVar(), None),
        ("Droga de Consumo Frecuente 3", tk.StringVar(), None),
        ("Localidad", tk.StringVar(), None),
        ("Ubicación Frecuente", tk.StringVar(), None),
        ("Género", tk.StringVar(), None),
        ("¿No es usuario de calle?", tk.BooleanVar(), None)
    ]

    for i, (label_text, var, callback) in enumerate(fields):
        label = ttk.Label(main_frame, text=label_text)
        label.grid(row=i, column=0, sticky=tk.W, pady=2)

        if label_text == "Departamento":
            departamento_var = var
            departamento_combobox = ttk.Combobox(main_frame, textvariable=departamento_var, state="readonly")
            departamento_combobox['values'] = list(departamentos_y_ciudades.keys())
            if callback:
                departamento_combobox.bind("<<ComboboxSelected>>", callback)
            departamento_combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text == "Ciudad":
            ciudad_var = var
            ciudad_combobox = ttk.Combobox(main_frame, textvariable=ciudad_var, state="readonly")
            ciudad_combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text == "Fecha de Nacimiento":
            fecha_nacimiento_var = var
            fecha_nacimiento_entry = DateEntry(main_frame, textvariable=fecha_nacimiento_var, date_pattern='dd/MM/yyyy', state="readonly")
            fecha_nacimiento_entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text == "¿No es usuario de calle?":
            no_es_usuario_de_calle_var = var
            no_es_usuario_de_calle_checkbutton = ttk.Checkbutton(main_frame, variable=no_es_usuario_de_calle_var)
            no_es_usuario_de_calle_checkbutton.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text in ["Primera Droga Consumida", "Droga de Consumo Frecuente 1", "Droga de Consumo Frecuente 2", "Droga de Consumo Frecuente 3"]:
            if label_text == "Primera Droga Consumida":
                primera_droga_var = var
            elif label_text == "Droga de Consumo Frecuente 1":
                droga_frecuente_1_var = var
            elif label_text == "Droga de Consumo Frecuente 2":
                droga_frecuente_2_var = var
            elif label_text == "Droga de Consumo Frecuente 3":
                droga_frecuente_3_var = var

            droga_combobox = ttk.Combobox(main_frame, textvariable=var, state="readonly")
            droga_combobox['values'] = opciones_drogas
            droga_combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text == "Localidad":
            localidad_var = var
            localidad_combobox = ttk.Combobox(main_frame, textvariable=localidad_var, state="readonly")
            localidad_combobox['values'] = opciones_localidad
            localidad_combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        elif label_text == "Género":
            genero_var = var
            genero_combobox = ttk.Combobox(main_frame, textvariable=genero_var, state="readonly")
            genero_combobox['values'] = opciones_genero
            genero_combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)
        else:
            entry = ttk.Entry(main_frame, textvariable=var)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=2)

            if label_text == "Nombre":
                nombre_entry = entry
            elif label_text == "Apellido":
                apellido_entry = entry
            elif label_text == "Año de Situación de Calle":
                ano_situacion_calle_entry = entry
            elif label_text == "Edad de Inicio de Consumo de Drogas":
                edad_inicio_drogas_entry = entry
            elif label_text == "Ubicación Frecuente":
                ubicacion_frecuente_entry = entry

    guardar_button = ttk.Button(main_frame, text="Guardar", command=guardar_datos)
    guardar_button.grid(row=len(fields), column=1, sticky=(tk.W, tk.E), pady=10)

def tomar_foto_y_guardar_datos():
    cap = cv2.VideoCapture(0)
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo leer el frame de la cámara.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

        cv2.imshow("Captura de foto - Presiona 's' para guardar", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Generar un ID común
            common_id = users_collection.estimated_document_count() + 1

            # Convertir el frame a bytes
            _, buffer = cv2.imencode('.jpg', frame)
            img_bytes = buffer.tobytes()

            # Guardar la foto en MongoDB usando GridFS
            try:
                photo_id = fs.put(img_bytes, filename=f"{common_id}_photo.jpg", common_id=common_id)
                print(f"Foto guardada con ID: {photo_id}")
            except Exception as e:
                print(f"Error al guardar la foto: {e}")
                messagebox.showerror("Error", f"No se pudo guardar la foto: {e}")

            # Guardar los datos faciales en MongoDB
            facial_data = [(p.x, p.y) for p in landmarks.parts()]
            facial_data_document = {
                "common_id": common_id,
                "facial_points": facial_data
            }
            facial_data_collection.insert_one(facial_data_document)

            registrar_usuario(common_id)
            break

    cap.release()
    cv2.destroyAllWindows()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Usuario")

main_frame = ttk.Frame(ventana, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
main_frame.columnconfigure(0, weight=1)

label = ttk.Label(main_frame, text="Presiona el botón para tomar una foto y registrar los datos del usuario")
label.grid(row=0, column=0, pady=10)

boton_tomar_foto = ttk.Button(main_frame, text="Tomar Foto y Registrar", command=tomar_foto_y_guardar_datos)
boton_tomar_foto.grid(row=1, column=0, pady=10)

ventana.mainloop()