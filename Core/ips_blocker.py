import os
import time
import threading
from abc import ABC, abstractmethod
from Database.conexion_pg import obtener_conexion

class EstrategiaBloqueo(ABC):
    @abstractmethod
    def bloquear_ip(self, ip):
        pass

class BloqueoWindows(EstrategiaBloqueo):
    def bloquear_ip(self, ip):
        # Mantenemos el log visual pero evitamos el os.system
        mensaje = f"[SIMULACIÓN PALADIN] IP {ip} marcada para bloqueo en Firewall (Omitido para demo sin admin)"
        print(mensaje)
        

class BloqueoLinux(EstrategiaBloqueo):
    def bloquear_ip(self, ip):
        print(f"[Paladin - Estrategia Linux] Simulación de bloqueo con iptables para: {ip}")

class EjecutorIPS:
    def __init__(self, estrategia: EstrategiaBloqueo):
        self.estrategia = estrategia

    def mitigar(self, ip):
        self.estrategia.bloquear_ip(ip)

# --- 2. MOTOR PRINCIPAL DE PALADIN ---
def iniciar_ips(gui): 
    print("[Paladin] Motor de Prevención de Intrusiones iniciado.")
    conexion = obtener_conexion()
    motor_defensa = EjecutorIPS(BloqueoWindows())

    while True:
        try:
            cursor = conexion.cursor()
            # FIX: Sincronizado con eventos_amenaza e ip_atacante
            cursor.execute("SELECT id, ip_atacante FROM eventos_amenaza WHERE estado_bloqueo = False")
            amenazas = cursor.fetchall()

            for amenaza in amenazas:
                id_evento = amenaza[0]
                ip_atacante = amenaza[1]

                motor_defensa.mitigar(ip_atacante)
                gui.log_paladin(f"> Bloqueo ejecutado: {ip_atacante}")
                
                # FIX: Actualizamos estado_bloqueo en eventos_amenaza
                cursor.execute("UPDATE eventos_amenaza SET estado_bloqueo = True WHERE id = %s", (id_evento,))
                conexion.commit()

            cursor.close()
            time.sleep(3) 
        except Exception as e:
            print(f"[Paladin] Error en el ciclo de escaneo: {e}")
            # FIX: Rollback crítico para no bloquear la BD
            if conexion:
                conexion.rollback()
            time.sleep(3)

def arrancar_en_hilo(gui):
    hilo_ips = threading.Thread(target=iniciar_ips, args=(gui,), daemon=True)
    hilo_ips.start()