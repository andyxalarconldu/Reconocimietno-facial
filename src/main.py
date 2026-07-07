import cv2
from embeddings.processor import procesar_y_guardar_registro, verificar_acceso

# ==========================================
# CONFIGURACIÓN DE LA CÁMARA
# ==========================================
# Aquí está la IP de tu celular con IP Webcam
URL_CAMARA = 1

def iniciar_app():
    print("Iniciando conexión con la cámara de tu celular...")
    captura = cv2.VideoCapture(URL_CAMARA)
    
    # Aquí guardaremos en memoria los números de tu rostro
    base_datos_embeddings = []
    modo_garita = False

    print("\n--- CONTROLES DEL SISTEMA ---")
    print("[F] Tomar Foto Frontal")
    print("[L] Tomar Foto Lateral")
    print("[V] Iniciar Escáner de Garita (Ponte los lentes aquí)")
    print("[Q] Salir del programa")

    while True:
        # Leer la cámara cuadro por cuadro
        exito, frame = captura.read()
        if not exito:
            print("Error conectando a la cámara. Revisa que IP Webcam esté encendido.")
            break

        # Copia de la imagen para dibujar los cuadros sin dañar la original
        frame_mostrar = frame.copy()

        if modo_garita:
            # === MODO GARITA (VERIFICACIÓN) ===
            resultados = verificar_acceso(frame, base_datos_embeddings)
            
            # Dibujar los resultados en la pantalla
            for res in resultados:
                top, right, bottom, left = res["ubicacion"]
                
                if res["acceso_permitido"]:
                    color = (0, 255, 0) # Verde (Acceso Correcto)
                    texto = "ACCESO PERMITIDO UCE"
                else:
                    color = (0, 0, 255) # Rojo (Desconocido)
                    texto = "DESCONOCIDO - ALERTA"
                
                # Dibujar el rectángulo alrededor de la cara
                cv2.rectangle(frame_mostrar, (left, top), (right, bottom), color, 2)
                # Dibujar el fondo del texto
                cv2.rectangle(frame_mostrar, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                # Escribir el texto
                cv2.putText(frame_mostrar, texto, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.putText(frame_mostrar, "MODO GARITA (Ponte Lentes)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            # === MODO REGISTRO ===
            cv2.putText(frame_mostrar, "MODO REGISTRO: Presiona F (Frontal) o L (Lateral)", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame_mostrar, f"Fotos guardadas en memoria: {len(base_datos_embeddings)}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Mostrar la ventana
        cv2.imshow('Prototipo IA - Proyecto UCE', frame_mostrar)
        
        # Leer qué tecla presionó el usuario
        tecla = cv2.waitKey(1) & 0xFF

        # --- Lógica de Botones ---
        if tecla == ord('f') or tecla == ord('F'):
            exito, emb, msg = procesar_y_guardar_registro(frame, "frontal")
            print(msg)
            if exito: base_datos_embeddings.append(emb)

        elif tecla == ord('l') or tecla == ord('L'):
            exito, emb, msg = procesar_y_guardar_registro(frame, "lateral")
            print(msg)
            if exito: base_datos_embeddings.append(emb)

        elif tecla == ord('v') or tecla == ord('V'):
            if base_datos_embeddings:
                print("\n>>> MODO GARITA ACTIVADO.")
                modo_garita = True
            else:
                print("⚠️ ERROR: Registra al menos una foto (presiona F) primero.")

        elif tecla == ord('q') or tecla == ord('Q'):
            print("Cerrando el sistema...")
            break

    # Apagar la cámara al salir
    captura.release()
    cv2.destroyAllWindows()

# Esto asegura que la app inicie solo si ejecutas este archivo
if __name__ == "__main__":
    iniciar_app()