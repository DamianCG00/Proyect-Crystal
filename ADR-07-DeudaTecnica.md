# ADR-07: Identificación y Documentación de Deudas Técnicas en Crystal

| Campo | Valor |
|---|---|
| Autor | Damian Coba G. |
| Fecha | 15/07/2026 |
| Estado | `Aceptado` |

---

## Contexto

Como parte de la revisión de calidad del ecosistema **Crystal**, se realizó una auditoría del módulo `Database/conexion_pg.py` y de los agentes que lo consumen (`Core/honeypot_server.py`, `Core/ips_blocker.py`). El objetivo fue identificar deuda técnica real, no forzada, que ya existe en el proyecto y que compromete la seguridad y la coherencia entre lo documentado en el ADR-06 y lo efectivamente implementado.

Se identificaron dos deudas técnicas, ambas originadas en el mismo archivo (`Database/conexion_pg.py`), pero de naturaleza distinta.

---

## Deuda Técnica #1: Credenciales de PostgreSQL escritas a mano en el código fuente

**Qué es:**
En `Database/conexion_pg.py`, la función `obtener_conexion()` contiene el host, la base de datos, el usuario y la contraseña de PostgreSQL como literales de texto plano dentro del código (`password="OrgBE11SqL34O#7"`), en lugar de leerlos desde variables de entorno o un archivo de configuración externo no versionado.

**Por qué existe:**
Fue una decisión consciente para cumplir con el tiempo de entrega del MVP (así lo reconoce el propio ADR-05, que prioriza *Rapid Prototyping* sobre buenas prácticas de configuración). Escribir la conexión directa fue la forma más rápida de tener Kalopsia y Paladin funcionando contra la base de datos sin invertir tiempo en un sistema de configuración.

**Costo de no pagarla:**
- La contraseña real de la base de datos queda expuesta en el historial de Git de un repositorio público en GitHub; cualquiera con acceso al repo puede conectarse a `crystal_db`.
- Cambiar de entorno (de la máquina local a un servidor de despliegue, o de un desarrollador a otro) obliga a editar el código fuente y volver a commitear, en vez de solo cambiar una variable.
- Si se rota la contraseña por seguridad, hay que modificar y redistribuir el código, no solo la configuración.

**Propuesta de solución:**
Migrar los cuatro valores a variables de entorno usando `os.environ.get()` (o la librería `python-dotenv` para desarrollo local), cargándolas desde un archivo `.env` que se agrega a `.gitignore`. Se deja un `.env.example` sin valores reales como referencia para el equipo. Esto es una refactorización de bajo riesgo porque no cambia la firma pública de `obtener_conexion()`, solo el origen de los datos.

```python
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "crystal_db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD")
    )
```

---

## Deuda Técnica #2: El patrón Singleton documentado en ADR-06 no está realmente implementado

**Qué es:**
El ADR-06 declara que se implementó el patrón **Singleton** para centralizar la conexión a PostgreSQL y evitar que un ataque masivo agote el *pool* de conexiones. Sin embargo, `obtener_conexion()` en `Database/conexion_pg.py` es una función simple que ejecuta `psycopg2.connect(...)` en cada invocación, sin guardar ni reutilizar ninguna instancia. Esto se confirma en `Core/honeypot_server.py`, donde cada conexión TCP entrante al honeypot dispara un `obtener_conexion()` nuevo, abriendo una conexión física distinta a la base de datos por cada intento de intrusión detectado.

**Por qué existe:**
Es un descuido no detectado a tiempo: el diseño del Singleton se documentó y se aprobó en el ADR-06 antes de completar su implementación real, y como el sistema funcionaba correctamente en las pruebas (poco volumen de conexiones simultáneas), la falta del patrón pasó desapercibida.

**Costo de no pagarla:**
- Es exactamente el escenario que el ADR-06 dice haber resuelto: durante un ataque de denegación de servicio con muchas conexiones simultáneas al honeypot, cada una abre su propia conexión a PostgreSQL, pudiendo agotar el límite de conexiones del servidor (`max_connections`) y tumbar tanto a Kalopsia como a Paladin.
- Genera una desconexión entre la documentación de arquitectura (ADR-06) y el código real, lo que puede inducir a error a cualquier desarrollador nuevo que confíe en el ADR para entender el sistema.

**Propuesta de solución:**
Implementar el Singleton real con una clase que mantenga la instancia de conexión en un atributo de clase y la reutilice si ya existe y sigue viva:

```python
import psycopg2

class ConexionDB:
    _instancia = None

    @classmethod
    def obtener_conexion(cls):
        if cls._instancia is None or cls._instancia.closed:
            cls._instancia = psycopg2.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                database=os.environ.get("DB_NAME", "crystal_db"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASSWORD")
            )
        return cls._instancia
```
Los módulos que hoy llaman a `obtener_conexion()` no necesitan cambiar su forma de uso, solo el import (`ConexionDB.obtener_conexion()`), lo que hace la migración incremental y de bajo riesgo.

---

## Clausula de Uso de IA

Este documento fue redactado de forma personal. Se utilizó inteligencia artificial como herramienta de apoyo en los siguientes aspectos específicos:

| Área de uso | Descripción |
| --- | --- |
| **Auditoría de código** | Se empleó la IA para revisar `Database/conexion_pg.py`, `Core/honeypot_server.py` y `Core/ips_blocker.py` en busca de deuda técnica real, contrastándolo con lo documentado en el ADR-06. |
| **Redacción del ADR** | Apoyo en la estructuración del documento siguiendo el mismo formato que ADR-05 y ADR-06, y en la redacción de las propuestas de solución. |
