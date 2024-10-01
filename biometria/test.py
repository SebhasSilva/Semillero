import numpy as np
import json

def calcular_similitud_facial(puntos1, puntos2):
    if len(puntos1) != len(puntos2):
        print(f"Longitudes diferentes: {len(puntos1)} vs {len(puntos2)}")
        return 0
    
    try:
        puntos1 = np.array(puntos1)
        puntos2 = np.array(puntos2)
        
        if puntos1.size == 0 or puntos2.size == 0:
            print("Uno de los conjuntos de puntos está vacío")
            return 0
        
        puntos1 = (puntos1 - puntos1.min(axis=0)) / (puntos1.max(axis=0) - puntos1.min(axis=0))
        puntos2 = (puntos2 - puntos2.min(axis=0)) / (puntos2.max(axis=0) - puntos2.min(axis=0))
        
        distancias = np.sqrt(np.sum((puntos1 - puntos2)**2, axis=1))
        similitud = 1 / (1 + np.mean(distancias))
        
        return similitud
    except Exception as e:
        print(f"Error en cálculo de similitud facial: {e}")
        return 0

# Datos de MongoDB
puntos_mongo = [
    [ 208, 220 ], [ 206, 234 ], [ 205, 249 ], [ 205, 265 ],
    [ 207, 280 ], [ 213, 294 ], [ 223, 305 ], [ 237, 314 ],
    [ 255, 318 ], [ 272, 318 ], [ 289, 312 ], [ 301, 302 ],
    [ 310, 289 ], [ 316, 274 ], [ 319, 259 ], [ 321, 245 ],
    [ 321, 231 ], [ 219, 203 ], [ 227, 196 ], [ 238, 193 ],
    [ 249, 196 ], [ 259, 200 ], [ 279, 204 ], [ 290, 202 ],
    [ 301, 202 ], [ 310, 206 ], [ 316, 215 ], [ 268, 215 ],
    [ 267, 223 ], [ 266, 232 ], [ 265, 241 ], [ 251, 248 ],
    [ 257, 250 ], [ 264, 253 ], [ 271, 252 ], [ 278, 250 ],
    [ 231, 216 ], [ 237, 214 ], [ 244, 215 ], [ 251, 219 ],
    [ 243, 218 ], [ 237, 217 ], [ 284, 222 ], [ 291, 221 ],
    [ 298, 222 ], [ 303, 225 ], [ 297, 225 ], [ 291, 224 ],
    [ 231, 267 ], [ 242, 260 ], [ 254, 259 ], [ 263, 261 ],
    [ 272, 260 ], [ 283, 264 ], [ 291, 273 ], [ 281, 283 ],
    [ 270, 286 ], [ 260, 286 ], [ 250, 284 ], [ 239, 278 ],
    [ 234, 268 ], [ 253, 265 ], [ 262, 267 ], [ 271, 267 ],
    [ 288, 273 ], [ 270, 278 ], [ 261, 278 ], [ 252, 276 ]
]

# Datos completos de Django
puntos_django_raw = "[{\"timestamp\": \"2024-09-29 18:48:26.709587\", \"landmarks\": [[470, 178], [452, 226], [437, 276], [428, 326], [431, 372], [448, 412], [473, 445], [505, 475], [544, 496], [589, 506], [630, 495], [670, 479], [707, 461], [741, 436], [770, 406], [791, 375], [808, 343], [535, 115], [569, 102], [608, 106], [641, 123], [669, 152], [724, 184], [754, 189], [782, 204], [801, 227], [805, 256], [680, 217], [671, 240], [662, 263], [653, 287], [603, 302], [616, 312], [628, 323], [645, 328], [662, 332], [558, 178], [583, 179], [604, 189], [618, 207], [595, 203], [573, 193], [708, 253], [732, 255], [751, 270], [762, 288], [741, 283], [722, 270], [539, 349], [574, 346], [606, 347], [616, 356], [630, 360], [645, 380], [651, 409], [628, 417], [606, 416], [592, 409], [579, 400], [556, 378], [550, 354], [598, 371], [609, 377], [622, 385], [641, 405], [616, 388], [603, 382], [592, 373]]}]"

# Procesar los datos de Django
puntos_django_data = json.loads(puntos_django_raw)
puntos_django = puntos_django_data[0]['landmarks']

print(f"Número de puntos en MongoDB: {len(puntos_mongo)}")
print(f"Número de puntos en Django: {len(puntos_django)}")

# Calcular la similitud
similitud = calcular_similitud_facial(puntos_mongo, puntos_django)

print(f"Similitud facial calculada: {similitud}")

# Probar diferentes umbrales
umbrales = [0.3, 0.5, 0.7, 0.9]
for umbral in umbrales:
    if similitud >= umbral:
        print(f"La similitud es mayor o igual que {umbral}")
    else:
        print(f"La similitud es menor que {umbral}")