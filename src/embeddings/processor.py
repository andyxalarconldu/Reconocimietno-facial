import os
import numpy as np
import datetime
from deepface import DeepFace

CARPETA_DATOS = os.path.join(os.getcwd(), "data", "fotos_registradas")
MODELO = "Facenet"

def registrar_log(nombre, estado):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {nombre} | {estado}")
    with open("logs_seguridad.txt", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {nombre} | {estado}\n")

def obtener_vector(ruta_img):
    try:
        rep = DeepFace.represent(img_path=ruta_img, model_name=MODELO, 
                                 enforce_detection=True, detector_backend="retinaface")
        return rep[0]["embedding"]
    except:
        return None

def cargar_base_datos():
    base = []
    if not os.path.exists(CARPETA_DATOS): return base
    for usuario in os.listdir(CARPETA_DATOS):
        ruta_usuario = os.path.join(CARPETA_DATOS, usuario)
        if os.path.isdir(ruta_usuario):
            for arch in os.listdir(ruta_usuario):
                if arch.endswith(".npy"):
                    vec = np.load(os.path.join(ruta_usuario, arch))
                    base.append({"nombre": usuario, "vector": vec})
    return base

def verificar_acceso(frame, base_datos, tolerancia=0.30):
    vec_actual = obtener_vector(frame)
    if vec_actual is None: return "NO DETECTADO", 1.0
    
    mejor_coincidencia = "DESCONOCIDO"
    menor_distancia = 1.0
    
    for reg in base_datos:
        dist = 1 - (np.dot(vec_actual, reg["vector"]) / (np.linalg.norm(vec_actual) * np.linalg.norm(reg["vector"])))
        if dist < menor_distancia:
            menor_distancia, mejor_coincidencia = dist, reg["nombre"]
            
    # Filtro estricto: Si la distancia es mayor a 0.30, se bloquea aunque se parezca
    if menor_distancia < tolerancia:
        registrar_log(mejor_coincidencia, "ACCESO OK")
        return mejor_coincidencia, menor_distancia
    else:
        registrar_log("Intruso", "ACCESO DENEGADO")
        return "ACCESO DENEGADO", menor_distancia