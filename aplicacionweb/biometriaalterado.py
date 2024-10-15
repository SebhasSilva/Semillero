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
import sqlite3
import threading
import time
import math
import os
import django
import json
import math
import numpy as np
import webbrowser
import secrets

def normalizar_texto(texto):
    return texto.lower().strip()

def normalizar_fecha(fecha_str):
    formatos = ["%d/%m/%Y", "%b. %d, %Y", "%Y-%m-%d"]
    for formato in formatos:
        try:
            return datetime.strptime(fecha_str, formato).date()
        except ValueError:
            continue
    return None

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aplicacionweb.settings")
django.setup()

# Importar modelos de Django
from users.models import StreetPerson
from photos.models import Photo

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb+srv://sebhassilva:12345@clustersemillero.xyem2ot.mongodb.net/ClusterSemillero?retryWrites=true&w=majority")
db = client['ClusterSemillero']
users_collection = db['users']
facial_data_collection = db['facial_data']
fs = gridfs.GridFS(db)

# Configuración para la funcionalidad de estadísticas
DJANGO_SERVER_URL = "http://127.0.0.1:8000"

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

def calcular_similitud_facial(puntos1, puntos2):
    print(f"Tipo de puntos1: {type(puntos1)}, Longitud: {len(puntos1)}")
    print(f"Tipo de puntos2: {type(puntos2)}, Longitud: {len(puntos2)}")

    if not puntos1 or not puntos2:
        print("Uno o ambos conjuntos de puntos están vacíos")
        return 0
    if len(puntos1) != len(puntos2):
        print(f"Longitudes diferentes: {len(puntos1)} vs {len(puntos2)}")
        return 0
    
    # Convertir a numpy arrays para cálculos más eficientes
    puntos1 = np.array(puntos1, dtype=np.float64)
    puntos2 = np.array(puntos2, dtype=np.float64)
    
    # Normalizar los puntos
    puntos1 = (puntos1 - puntos1.min(axis=0)) / (puntos1.max(axis=0) - puntos1.min(axis=0))
    puntos2 = (puntos2 - puntos2.min(axis=0)) / (puntos2.max(axis=0) - puntos2.min(axis=0))
    
    # Calcular distancia euclidiana media directamente
    distancia_media = np.mean(np.sqrt(np.sum((puntos1 - puntos2)**2, axis=1)))
    
    # Calcular similitud
    similitud = 1 / (1 + distancia_media)
    
    return similitud

# Función para comparar datos del formulario
from Levenshtein import ratio

def comparar_cadenas(str1, str2):
    str1_norm = normalizar_texto(str1)
    str2_norm = normalizar_texto(str2)
    return ratio(str1_norm, str2_norm)

def comparar_datos_formulario(datos_mongo, datos_django):
    campos = [
        ('nombre', 'first_name', 0.20),
        ('apellido', 'last_name', 0.20),
        ('ciudad', 'birth_city', 0.10),
        ('genero', 'gender', 0.10),
        ('fecha_nacimiento', 'birth_date', 0.10) 
    ]
    similitud_total = 0
    for campo_mongo, campo_django, peso in campos:
        valor_mongo = str(datos_mongo.get(campo_mongo, ''))
        valor_django = str(getattr(datos_django, campo_django, ''))
        
        if campo_mongo == 'fecha_nacimiento':
            fecha_mongo = normalizar_fecha(valor_mongo)
            fecha_django = normalizar_fecha(valor_django)
            similitud = 1 if fecha_mongo == fecha_django else 0
        else:
            similitud = comparar_cadenas(valor_mongo, valor_django)
        
        similitud_total += similitud * peso
        print(f"Campo: {campo_mongo}, Similitud: {similitud}, Peso: {peso}")
    
    return similitud_total

def buscar_coincidencias(silent=False):
    usuarios_mongo = users_collection.find()
    resultados = []
    
    print(f"Número de usuarios en MongoDB: {users_collection.count_documents({})}")
    print(f"Número de StreetPersons en Django: {StreetPerson.objects.count()}")
    
    for usuario_mongo in usuarios_mongo:
        street_persons = StreetPerson.objects.all()
        coincidencias = []
        
        for street_person in street_persons:
            similitud_formulario = comparar_datos_formulario(usuario_mongo, street_person)
            
            facial_mongo = facial_data_collection.find_one({"common_id": usuario_mongo['common_id']})
            facial_django = Photo.objects.filter(profile=street_person.profile).first()
           
            similitud_facial = 0
            if facial_mongo and facial_django:
                print(f"facial_mongo: {facial_mongo}")
                print(f"facial_django: {facial_django}")
                try:
                    facial_points_mongo = facial_mongo.get('facial_points', [])
                    
                    # Acceder a los landmarks a través de la relación
                    landmarks = getattr(facial_django, 'landmarks', None)
                    if landmarks:
                        facial_points_django = json.loads(landmarks.data)
                        
                        if isinstance(facial_points_django, list) and len(facial_points_django) > 0:
                            if isinstance(facial_points_django[0], dict):
                                facial_points_django = facial_points_django[0].get('landmarks', [])
                        
                        if facial_points_mongo and facial_points_django:
                            print(f"Número de puntos en MongoDB: {len(facial_points_mongo)}")
                            print(f"Número de puntos en Django: {len(facial_points_django)}")
                            similitud_facial = calcular_similitud_facial(facial_points_mongo, facial_points_django)
                            print(f"Similitud facial calculada: {similitud_facial}")
                            if similitud_facial >= 0.8:  #Umbral de similitud facial
                                similitud_facial = similitud_facial
                            else:
                                similitud_facial = 0
                        else:
                            print(f"Datos faciales faltantes para StreetPerson {street_person.id} o usuario MongoDB {usuario_mongo['common_id']}")
                    else:
                        print(f"No se encontraron landmarks para la foto de StreetPerson {street_person.id}")
                except json.JSONDecodeError:
                    print(f"Error al decodificar datos faciales de Django para StreetPerson {street_person.id}")
                except Exception as e:
                    print(f"Error al procesar datos faciales: {str(e)}")
            
            similitud_total = similitud_formulario + (0.3 * similitud_facial)
            
            if similitud_total >= 0.6:
                coincidencias.append({
                    'street_person': street_person,
                    'similitud_total': similitud_total,
                    'similitud_formulario': similitud_formulario,
                    'similitud_facial': similitud_facial,
                    'datos_mongo': usuario_mongo,
                    'datos_django': street_person
                })
        
        mejores_coincidencias = sorted(coincidencias, key=lambda x: x['similitud_total'], reverse=True)[:3]
        
        if mejores_coincidencias:
            resultados.append({
                'usuario_mongo': usuario_mongo,
                'mejores_coincidencias': mejores_coincidencias
            })
    return resultados

def verificar_decision_previa(common_id, silent=False):
    usuario = users_collection.find_one({'common_id': common_id})
    if 'decisiones_reencuentro' in usuario:
        ultima_decision = usuario['decisiones_reencuentro'][-1]
        if not silent:
            print(f"Nota: Esta persona decidió no re-encontrarse con su familia en {ultima_decision['fecha']}.")
        return ultima_decision
    return None

def mostrar_resultados_y_obtener_decision(resultados):
    if not resultados:
        messagebox.showinfo("Sin coincidencias", "No se encontraron coincidencias.")
        return
    for resultado in resultados:
        decision_previa = verificar_decision_previa(resultado['usuario_mongo']['common_id'])
        
        mensaje = f"Usuario: {resultado['usuario_mongo']['nombre']} {resultado['usuario_mongo']['apellido']}\n\n"
        if decision_previa:
            mensaje += f"Decisión previa: No re-encontrarse (fecha: {decision_previa['fecha']})\n\n"
        mensaje += "Mejores coincidencias:\n"
        for coincidencia in resultado['mejores_coincidencias']:
            street_person = coincidencia['street_person']
            mensaje += f"  - {street_person.first_name} {street_person.last_name}\n"
            mensaje += f"    Similitud total: {coincidencia['similitud_total']:.2f}\n"
            mensaje += f"    Similitud formulario: {coincidencia['similitud_formulario']:.2f}\n"
            mensaje += f"    Similitud facial: {coincidencia['similitud_facial']:.2f}\n"
            mensaje += f"    Datos MongoDB: Nombre: {coincidencia['datos_mongo'].get('nombre')}, Apellido: {coincidencia['datos_mongo'].get('apellido')}, Ciudad: {coincidencia['datos_mongo'].get('ciudad')}, Género: {coincidencia['datos_mongo'].get('genero')}\n"
            mensaje += f"    Datos Django: Nombre: {street_person.first_name}, Apellido: {street_person.last_name}, Ciudad: {street_person.birth_city}, Género: {street_person.gender}\n\n"
        
        decision = messagebox.askyesno("Decisión de Reencuentro", 
                                       mensaje + "\n¿La persona desea re-encontrarse con su familia?")
        
        if decision:
            enviar_notificacion(resultado['usuario_mongo']['common_id'])
            messagebox.showinfo("Notificación Enviada", "Se ha enviado una notificación a Integración Social.")
        else:
            guardar_decision_negativa(resultado['usuario_mongo']['common_id'])
            messagebox.showinfo("Decisión Guardada", "Se ha guardado la decisión. Se recordará en futuras interacciones.")

def enviar_notificacion(common_id):
    # Aquí iría el código para enviar la notificación a Integración Social
    print(f"Enviando notificación para el usuario con common_id: {common_id}")

def guardar_decision_negativa(common_id):
    decision_reencuentro = {
        'fecha': datetime.now(),
        'decision': 'no'
    }
    users_collection.update_one(
        {'common_id': common_id},
        {'$push': {'decisiones_reencuentro': decision_reencuentro}}
    )
    print(f"Decisión negativa guardada para el usuario con common_id: {common_id}")

def mostrar_notificacion_nuevas_coincidencias(resultados):
    if resultados:
        messagebox.showinfo("Nuevas Coincidencias", f"Se han encontrado {len(resultados)} nuevas coincidencias.")

def generar_token_temporal():
    return secrets.token_urlsafe(32)

def abrir_estadisticas():
    token = generar_token_temporal()
    url = f"{DJANGO_SERVER_URL}/estadisticas/?token={token}"
    webbrowser.open(url)

# Añadir esta función si no está definida
def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Registro de Usuario y Búsqueda de Coincidencias")

    main_frame = ttk.Frame(ventana, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)

    label = ttk.Label(main_frame, text="Presiona el botón para tomar una foto y registrar los datos del usuario")
    label.grid(row=0, column=0, pady=10)

    # Añadir el checkbox de autorización
    autorizacion_var = tk.BooleanVar()
    autorizacion_checkbox = ttk.Checkbutton(main_frame, text="Autorización para el tratamiento de datos personales", variable=autorizacion_var)
    autorizacion_checkbox.grid(row=1, column=0, pady=5)

    # Modificar la función del botón para verificar la autorización
    def tomar_foto_con_autorizacion():
        if autorizacion_var.get():
            tomar_foto_y_guardar_datos()
        else:
            messagebox.showerror("Error", "Debe autorizar el tratamiento de datos personales para continuar.")

    boton_tomar_foto = ttk.Button(main_frame, text="Tomar Foto y Registrar", command=tomar_foto_con_autorizacion)
    boton_tomar_foto.grid(row=2, column=0, pady=10)

    boton_buscar = ttk.Button(main_frame, text="Buscar Coincidencias", command=mostrar_resultados_busqueda)
    boton_buscar.grid(row=3, column=0, pady=10)

    boton_estadisticas = ttk.Button(main_frame, text="Ver Estadísticas", command=abrir_estadisticas)
    boton_estadisticas.grid(row=4, column=0, pady=10)

    return ventana

def mostrar_resultados_busqueda():
    resultados = buscar_coincidencias()
    ventana.after(0, lambda: mostrar_resultados_y_obtener_decision(resultados))

if __name__ == "__main__":
    # Creación de la ventana principal
    ventana = crear_ventana_principal()

    ventana.mainloop()