import socket
import threading
from Database.conexion_pg import obtener_conexion

def iniciar_honeypot(gui): 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    gui.log_kalopsia("Honeypot escuchando en puerto 8080...")
    
    while True:
        conn, addr = server.accept()
        ip = addr[0]
        
        try:
            # Intentamos leer qué es lo que busca el atacante (Ej. GET /Saludar HTTP/1.1)
            peticion = conn.recv(1024).decode('utf-8', errors='ignore')
            objetivo = "Puerto 8080 (Petición vacía/Escaneo TCP)"
            
            if peticion:
                # Tomamos solo la primera línea de la petición web
                primera_linea = peticion.split('\n')[0].strip()
                objetivo = primera_linea
            
            # Mostramos el objetivo específico en la terminal verde
            gui.log_kalopsia(f"Intrusión: {ip}")
            gui.log_kalopsia(f"  -> Objetivo: {objetivo}")
            
            # Guardamos esto en la BD (lo metemos en la columna tipo_ataque)
            tipo_ataque_bd = f"Web: {objetivo}"[:50] # Limitamos a 50 caracteres por si acaso
            
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO eventos_amenaza (ip_atacante, tipo_ataque, estado_bloqueo) VALUES (%s, %s, %s)", (ip, tipo_ataque_bd, False))
            conexion.commit()
            cursor.close()
        except Exception as e:
            gui.log_kalopsia(f"Error BD Kalopsia: {e}")
        finally:
            conn.close()

def arrancar_en_hilo(gui): 
    hilo = threading.Thread(target=iniciar_honeypot, args=(gui,), daemon=True)
    hilo.start()