import os
import time
from abc import ABC, abstractmethod
from Database.conexion_pg import obtener_conexion


class EstrategiaBloqueo(ABC):
    @abstractmethod
    def bloquear_ip(self, ip):
        pass

class BloqueoWindows(EstrategiaBloqueo):
    def bloquear_ip(self, ip):
        print(f"[Paladin - Estrategia Windows] Bloqueando IP: {ip}")
        os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')

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
            
            
            cursor.execute("SELECT id, ip_atacante FROM eventos_amenaza WHERE estado_bloqueo = False")
            amenazas = cursor.fetchall()

            for amenaza in amenazas:
                id_evento = amenaza[0]
                ip_atacante = amenaza[1]

                motor_defensa.mitigar(ip_atacante)

                gui.log_paladin(f"> Bloqueo simulado exitosamente: {ip_atacante}")

                
                cursor.execute("UPDATE eventos_amenaza SET estado_bloqueo = True WHERE id = %s", (id_evento,))
                conexion.commit()

            cursor.close()
            time.sleep(3) 
            
        except Exception as e:
            print(f"[Paladin] Error en el ciclo de escaneo: {e}")
            time.sleep(3)