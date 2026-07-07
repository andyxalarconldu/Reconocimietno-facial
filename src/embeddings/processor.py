import cv2
import face_recognition
import os
import time
import numpy as np

CARPETA_DATOS = os.path.join(os.getcwd(), "data", "fotos_registradas")
os.makedirs(CARPETA_DATOS, exist_ok=True)

def preparar_imagen_para_dlib(frame):
    # 1. Convertir los colores al formato requerido
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except Exception:
        rgb_frame = frame
        
    # 2. Reconstruir la matriz desde cero obligando a que sea de 8 bits (uint8)
    # El parametro copy=True destruye metadatos anteriores y limpia la fragmentacion
    imagen_limpia = np.array(rgb_frame, dtype=np.uint8, copy=True)
    
    # 3. Empaquetar como bloque solido
    return np.ascontiguousarray(imagen_limpia)


def procesar_y_guardar_registro(frame, tipo_foto):
    
    rgb_frame = preparar_imagen_para_dlib(frame)
    
    ubicaciones = face_recognition.face_locations(rgb_frame)
    
    if not ubicaciones:
        return False, None, "[ERROR] No se detecto ningun rostro. Intenta de nuevo."
    
    embedding = face_recognition.face_encodings(rgb_frame, ubicaciones)[0]
    
    timestamp = int(time.time())
    nombre_archivo = f"registro_{tipo_foto}_{timestamp}.jpg"
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    
    cv2.imwrite(ruta_completa, frame)
    
    return True, embedding, f"[EXITO] Foto {tipo_foto} guardada correctamente ({nombre_archivo})"


def verificar_acceso(frame, base_embeddings_conocidos, tolerancia=0.6):
    
    rgb_frame = preparar_imagen_para_dlib(frame)
    
    ubicaciones = face_recognition.face_locations(rgb_frame)
    resultados = []
    
    if not ubicaciones:
        return resultados

    embeddings_prueba = face_recognition.face_encodings(rgb_frame, ubicaciones)

    for (top, right, bottom, left), emb_prueba in zip(ubicaciones, embeddings_prueba):
        coincidencias = face_recognition.compare_faces(base_embeddings_conocidos, emb_prueba, tolerance=tolerancia)
        
        es_usuario_valido = True in coincidencias
        
        resultados.append({
            "ubicacion": (top, right, bottom, left),
            "acceso_permitido": es_usuario_valido
        })
        
    return resultados