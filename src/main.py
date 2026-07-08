import cv2
from embeddings.processor import cargar_base_datos, verificar_acceso

URL_CAMARA = "http://192.168.100.69:4747/video"
base_datos = cargar_base_datos()
captura = cv2.VideoCapture(URL_CAMARA)

modo_garita = False
frame_count = 0
nombre = "..."

print("\n--- SISTEMA DE SEGURIDAD OPERATIVO ---")
print("Presiona 'V' para activar/desactivar, 'Q' para salir.")

while True:
    exito, frame = captura.read()
    if not exito: break
    
    # Rotación a 90 grados contra reloj para corregir tu sensor
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame_small = cv2.resize(frame, (320, 240))
    frame_display = frame.copy()

    if modo_garita:
        frame_count += 1
        # Analizar cada 10 frames para mantener la fluidez del video
        if frame_count % 10 == 0:
            nombre, distancia = verificar_acceso(frame_small, base_datos)
        
        # Visualización de estados
        if nombre == "ACCESO DENEGADO" or nombre == "DESCONOCIDO" or nombre == "NO DETECTADO":
            cv2.putText(frame_display, "ACCESO DENEGADO", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        else:
            cv2.putText(frame_display, f"OK - BIENVENIDO: {nombre}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            
    else:
        cv2.putText(frame_display, "SISTEMA EN ESPERA - PRESIONA 'V'", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('PROTOTIPO UCE - IA', frame_display)
    
    key = cv2.waitKey(1)
    if key == ord('q'): break
    if key == ord('v'): modo_garita = not modo_garita

captura.release()
cv2.destroyAllWindows()