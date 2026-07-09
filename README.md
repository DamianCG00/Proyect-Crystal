# 🛡️ Ecosistema de Ciberseguridad: Crystal

## 👨‍💻 Información del Autor
* **Desarrollador:** Damian Coba G.
* **Proyecto:** Crystal (Módulos Kalopsia y Paladín)

---

## 📖 Descripción del Proyecto
**Crystal** es un ecosistema avanzado de ciberseguridad diseñado para detectar, registrar y mitigar amenazas en tiempo real. El desarrollo del proyecto se centra en el "blindaje" del código y la gestión de transacciones de base de datos robustas, garantizando la máxima integridad del sistema frente a posibles ataques o vulnerabilidades.

El núcleo de la arquitectura se divide en dos módulos principales que interactúan de forma continua:

* **👁️ Kalopsia (Módulo Sensor):** Es el componente de detección y monitoreo. Opera mediante servidores trampa (`honeypot_server.py`) encargados de atraer, identificar y registrar tráfico malicioso o anomalías en la red antes de que alcancen el sistema real.
* **⚔️ Paladín (Actuador IPS):** Es el Sistema de Prevención de Intrusiones (`ips_blocker.py`). Responde de manera automática a las alertas de seguridad generadas por Kalopsia, ejecutando rutinas de mitigación y aplicando reglas de bloqueo para neutralizar las amenazas de forma inmediata.

---

## 🛠️ Arquitectura y Componentes
El proyecto implementa una solución híbrida que combina scripts de seguridad en Python con una interfaz de programación robusta.

* **Backend de Ciberseguridad (Python):** 
  * Orquestación principal e interfaz (`main.py`, `ventana_principal.py`).
  * Sensores y bloqueadores (`honeypot_server.py`, `ips_blocker.py`).
* **API de Integración:** Componente `.NET` (`Crystal.Api`) para la gestión y comunicación de alertas.
* **Persistencia de Datos:** Conexiones seguras a bases de datos PostgreSQL (`conexion_pg.py`) garantizando el blindaje en las transacciones.
* **Documentación y Decisiones Arquitectónicas:** El proyecto incluye archivos ADR (Architecture Decision Records) que respaldan las decisiones técnicas, incluyendo la implementación de Patrones GoF (`ADR-05-Damian-Coba.md`, `ADR-06-PatronesGOF.md`).

---

## 🚀 Ejecución del Sistema

Para inicializar el ecosistema Crystal (levantar sensores, habilitar actuadores y conectar la API), ejecuta el script de inicialización por lotes incluido en la raíz del repositorio:

```bash
iniciar_Crystal.bat