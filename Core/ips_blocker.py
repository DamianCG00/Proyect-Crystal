import time
import threading
from Database.conexion_pg import obtener_conexion

def motor_ips(gui): # <-- Agregamos 'gui' como argumento
    gui.log_paladin("Motor IPS de mitigación iniciado...")
    while True:
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, ip_atacante FROM eventos_amenaza WHERE estado_bloqueo = FALSE")
            amenazas = cursor.fetchall()
            
            for amenaza in amenazas:
                id_am, ip = amenaza
                # Cambiamos print por log_paladin
                gui.log_paladin(f"COMANDO EJECUTADO: netsh advfirewall firewall add rule name='Bloqueo {ip}' dir=in action=block remoteip={ip}")
                cursor.execute("UPDATE eventos_amenaza SET estado_bloqueo = TRUE WHERE id = %s", (id_am,))
            
            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            gui.log_paladin(f"Error en motor IPS: {e}")
        
        time.sleep(3)

def arrancar_en_hilo(gui): # <-- Recibe la GUI desde main.py
    # Usamos args=(gui,) para pasar el objeto al hilo secundario
    hilo = threading.Thread(target=motor_ips, args=(gui,), daemon=True)
    hilo.start()