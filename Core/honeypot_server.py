import socket
import threading
from Database.conexion_pg import obtener_conexion

def iniciar_honeypot(gui): # <-- Agregamos 'gui' como argumento
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8080))
    server.listen(5)
    gui.log_kalopsia("Honeypot escuchando en puerto 8080...")
    
    while True:
        conn, addr = server.accept()
        ip = addr[0]
        # Cambiamos print por log_kalopsia
        gui.log_kalopsia(f"Intrusión detectada desde: {ip}")
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO eventos_amenaza (ip_atacante, tipo_ataque) VALUES (%s, %s)", (ip, "Escaneo de Puerto 8080"))
            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            gui.log_kalopsia(f"Error BD Kalopsia: {e}")
        conn.close()

def arrancar_en_hilo(gui): # <-- Recibe la GUI desde main.py
    # Usamos args=(gui,) para pasar el objeto al hilo secundario
    hilo = threading.Thread(target=iniciar_honeypot, args=(gui,), daemon=True)
    hilo.start()