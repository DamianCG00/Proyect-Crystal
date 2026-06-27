import time
import os
from abc import ABC, abstractmethod
from Database.conexion_pg import obtener_conexion

# --- 1. PATRÓN STRATEGY (CATEGORÍA: COMPORTAMIENTO) ---
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
        # os.system(f'iptables -A INPUT -s {ip} -j DROP')

class EjecutorIPS:
    def __init__(self, estrategia: EstrategiaBloqueo):
        self.estrategia = estrategia

    def mitigar(self, ip):
        self.estrategia.bloquear_ip(ip)


# --- 2. MOTOR PRINCIPAL DE PALADIN ---
def iniciar_ips():
    print("[Paladin] Motor de Prevención de Intrusiones iniciado.")
    
    # Usamos el Singleton para obtener la conexión
    conexion = obtener_conexion()
    
    # AQUÍ ES DONDE AGREGAS LA INICIALIZACIÓN DE LA ESTRATEGIA
    motor_defensa = EjecutorIPS(BloqueoWindows())

    while True:
        try:
            cursor = conexion.cursor()
            
            # (Ajusta los nombres de esta consulta si tus tablas o columnas se llaman diferente)
            cursor.execute("SELECT id, ip_origen FROM eventos WHERE bloqueado = False")
            amenazas = cursor.fetchall()

            for amenaza in amenazas:
                id_evento = amenaza[0]
                ip_atacante = amenaza[1]

                # AQUÍ ES DONDE EJECUTAS EL BLOQUEO USANDO EL PATRÓN
                motor_defensa.mitigar(ip_atacante)

                # Actualizamos la base de datos para marcarla como bloqueada
                cursor.execute("UPDATE eventos SET bloqueado = True WHERE id = %s", (id_evento,))
                conexion.commit()

            cursor.close()
            time.sleep(3) # Pausa de 3 segundos antes del próximo escaneo
            
        except Exception as e:
            print(f"[Paladin] Error en el ciclo de escaneo: {e}")
            time.sleep(3)