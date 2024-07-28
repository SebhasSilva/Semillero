import cv2
import dlib
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from pymongo import MongoClient
import gridfs

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

opciones_drogas = ["N/A", "Alcohol", "Cigarrillo", "Marihuana", "Cocaína", "Heroína", "LSD", "Éxtasis", "Metanfetamina", "Bazuco"]

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
        no_es_usuario_de_calle = no_es_usuario_de_calle_var.get()

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
            "genero": genero,
            "no_es_usuario_de_calle": no_es_usuario_de_calle
        }

        # Asegúrate de que common_id esté correctamente definido
        if common_id is None:
            messagebox.showwarning("Advertencia", "ID del usuario no está definido.")
            return

        # Actualizar el registro en la base de datos
        users_collection.update_one({"_id": common_id}, {"$set": user_data}, upsert=True)
        messagebox.showinfo("Información", "Usuario registrado exitosamente.")
        dialogo.destroy()
        ventana.quit()  # Cerrar la ventana principal

    def actualizar_ciudades(*args):
        departamento = departamento_var.get()
        ciudades = departamentos_y_ciudades.get(departamento, [])
        ciudad_combobox['values'] = ciudades
        if not ciudades:
            ciudad_var.set('')
        else:
            ciudad_var.set(ciudades[0])

    dialogo = tk.Toplevel()
    dialogo.title("Registro de Usuario")

    # Crear un frame para contener el formulario
    frame_formulario = ttk.Frame(dialogo, padding="10")
    frame_formulario.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Variables de control para los campos del formulario
    nombre_var = tk.StringVar()
    apellido_var = tk.StringVar()
    departamento_var = tk.StringVar()
    ciudad_var = tk.StringVar()
    fecha_nacimiento_var = tk.StringVar()
    ano_situacion_calle_var = tk.StringVar()
    edad_inicio_drogas_var = tk.StringVar()
    primera_droga_var = tk.StringVar()
    droga_frecuente_1_var = tk.StringVar()
    droga_frecuente_2_var = tk.StringVar()
    droga_frecuente_3_var = tk.StringVar()
    localidad_var = tk.StringVar()
    ubicacion_frecuente_var = tk.StringVar()
    genero_var = tk.StringVar()
    no_es_usuario_de_calle_var = tk.StringVar()

    # Campos del formulario
    ttk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
    nombre_entry = ttk.Entry(frame_formulario, textvariable=nombre_var)
    nombre_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Apellido:").grid(row=1, column=0, sticky=tk.W)
    apellido_entry = ttk.Entry(frame_formulario, textvariable=apellido_var)
    apellido_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Departamento:").grid(row=2, column=0, sticky=tk.W)
    departamento_combobox = ttk.Combobox(frame_formulario, textvariable=departamento_var, values=list(departamentos_y_ciudades.keys()))
    departamento_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E))
    departamento_combobox.bind("<<ComboboxSelected>>", actualizar_ciudades)

    ttk.Label(frame_formulario, text="Ciudad:").grid(row=3, column=0, sticky=tk.W)
    ciudad_combobox = ttk.Combobox(frame_formulario, textvariable=ciudad_var)
    ciudad_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Fecha de Nacimiento:").grid(row=4, column=0, sticky=tk.W)
    fecha_nacimiento_entry = DateEntry(frame_formulario, textvariable=fecha_nacimiento_var, date_pattern='dd/MM/yyyy')
    fecha_nacimiento_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Año Situación de Calle:").grid(row=5, column=0, sticky=tk.W)
    ano_situacion_calle_entry = ttk.Entry(frame_formulario, textvariable=ano_situacion_calle_var)
    ano_situacion_calle_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Edad Inicio de Drogas:").grid(row=6, column=0, sticky=tk.W)
    edad_inicio_drogas_entry = ttk.Entry(frame_formulario, textvariable=edad_inicio_drogas_var)
    edad_inicio_drogas_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Primera Droga Consumida:").grid(row=7, column=0, sticky=tk.W)
    primera_droga_combobox = ttk.Combobox(frame_formulario, textvariable=primera_droga_var, values=opciones_drogas)
    primera_droga_combobox.grid(row=7, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Droga Frecuente 1:").grid(row=8, column=0, sticky=tk.W)
    droga_frecuente_1_combobox = ttk.Combobox(frame_formulario, textvariable=droga_frecuente_1_var, values=opciones_drogas)
    droga_frecuente_1_combobox.grid(row=8, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Droga Frecuente 2:").grid(row=9, column=0, sticky=tk.W)
    droga_frecuente_2_combobox = ttk.Combobox(frame_formulario, textvariable=droga_frecuente_2_var, values=opciones_drogas)
    droga_frecuente_2_combobox.grid(row=9, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Droga Frecuente 3:").grid(row=10, column=0, sticky=tk.W)
    droga_frecuente_3_combobox = ttk.Combobox(frame_formulario, textvariable=droga_frecuente_3_var, values=opciones_drogas)
    droga_frecuente_3_combobox.grid(row=10, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Localidad:").grid(row=11, column=0, sticky=tk.W)
    localidad_combobox = ttk.Combobox(frame_formulario, textvariable=localidad_var, values=opciones_localidad)
    localidad_combobox.grid(row=11, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Ubicación Frecuente:").grid(row=12, column=0, sticky=tk.W)
    ubicacion_frecuente_entry = ttk.Entry(frame_formulario, textvariable=ubicacion_frecuente_var)
    ubicacion_frecuente_entry.grid(row=12, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="Género:").grid(row=13, column=0, sticky=tk.W)
    genero_combobox = ttk.Combobox(frame_formulario, textvariable=genero_var, values=opciones_genero)
    genero_combobox.grid(row=13, column=1, sticky=(tk.W, tk.E))

    ttk.Label(frame_formulario, text="No es Usuario de Calle:").grid(row=14, column=0, sticky=tk.W)
    no_es_usuario_de_calle_checkbox = ttk.Checkbutton(frame_formulario, variable=no_es_usuario_de_calle_var, onvalue="Sí", offvalue="No")
    no_es_usuario_de_calle_checkbox.grid(row=14, column=1, sticky=(tk.W, tk.E))

    ttk.Button(frame_formulario, text="Guardar", command=guardar_datos).grid(row=15, column=0, columnspan=2)

    dialogo.transient(ventana)  # Hacer que el cuadro de diálogo sea modal
    dialogo.grab_set()
    ventana.wait_window(dialogo)

# Función para capturar foto y registrar usuario
def capturar_foto_y_registrar_usuario():
    cap = cv2.VideoCapture(0)
    detector_rostros = dlib.get_frontal_face_detector()
    
    common_id = None

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rostros = detector_rostros(frame_rgb)
        
        for rostro in rostros:
            x, y, w, h = (rostro.left(), rostro.top(), rostro.width(), rostro.height())
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.imshow("Captura de Rostros - Presiona 'c' para capturar", frame)
        
        key = cv2.waitKey(1)
        if key == ord('c') and rostros:
            rostro_capturado = frame[y:y + h, x:x + w]
            _, img_encoded = cv2.imencode('.jpg', rostro_capturado)
            common_id = fs.put(img_encoded.tobytes(), filename='rostro.jpg')
            break
    
    cap.release()
    cv2.destroyAllWindows()

    if common_id is not None:
        registrar_usuario(common_id)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Usuarios")
ventana.geometry("400x200")

# Botón para capturar foto y registrar usuario
boton_registrar = ttk.Button(ventana, text="Capturar Foto y Registrar Usuario", command=capturar_foto_y_registrar_usuario)
boton_registrar.pack(expand=True)

ventana.mainloop()