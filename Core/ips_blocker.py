import time
import threading
from Database.conexion_pg import obtener_conexion

def motor_ips():
    print("[Paladin] Motor IPS de mitigación iniciado...")
    while True:
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, ip_atacante FROM eventos_amenaza WHERE estado_bloqueo = FALSE")
            amenazas = cursor.fetchall()
            
            for amenaza in amenazas:
                id_am, ip = amenaza
                print(f"[Paladin] COMANDO EJECUTADO: netsh advfirewall firewall add rule name='Bloqueo {ip}' dir=in action=block remoteip={ip}")
                cursor.execute("UPDATE eventos_amenaza SET estado_bloqueo = TRUE WHERE id = %s", (id_am,))
            
            conexion.commit()
            cursor.close()
            conexion.close()
        except Exception as e:
            pass
        
        time.sleep(3)

def arrancar_en_hilo():
    hilo = threading.Thread(target=motor_ips, daemon=True)
    hilo.start()