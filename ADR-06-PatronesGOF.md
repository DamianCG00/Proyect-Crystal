# ADR-06: Implementación de Patrones GOF (Singleton y Strategy) en Crystal

| Campo | Valor |
|---|---|
| Autor | Damian Coba G. |
| Fecha | 26/06/2026 |
| Estado | `Reemplazo del ADR 5` |

---

## Contexto

Como parte de la evolución arquitectónica del ecosistema **Crystal**, se requería resolver dos problemas críticos en los agentes locales: optimizar la gestión de conexiones a PostgreSQL (para evitar que un ataque masivo agote los recursos del servidor) y desacoplar la lógica de mitigación del motor IPS (Paladin), la cual estaba limitada exclusivamente a comandos de firewall en Windows. El objetivo es estabilizar el sistema e inyectar patrones formales (GOF) para soportar escalabilidad multiplataforma.

---

## Decisión

Se decidió implementar dos patrones de diseño de categorías distintas:
1. **Singleton (Creacional):** Para centralizar la instancia de conexión a la base de datos PostgreSQL.
2. **Strategy (De Comportamiento):** Para abstraer el algoritmo de bloqueo de IPs a través de una interfaz común.

### ¿Por qué?

- El **Singleton** garantiza que Kalopsia y Paladin compartan un único acceso a la base de datos. La característica concreta que resuelve el problema es su capacidad de retornar una instancia en memoria si ya existe, evitando colapsar el *pool* de conexiones durante un ataque de denegación de servicio (DoS).
- El **Strategy** permite inyectar el método de bloqueo (`BloqueoWindows` o `BloqueoLinux`) en tiempo de ejecución. La característica concreta que resuelve el problema es la eliminación de condicionales anidados, respetando el principio Open/Closed y permitiendo que el bucle de detección funcione sin importar el sistema operativo host.

### Alternativas consideradas

| Alternativa | Por qué la descarté |
|-------------|---------------------|
| **Inyección Manual de Dependencias** | Pasar el objeto de conexión como parámetro por todas las funciones de los hilos hubiera ensuciado el código y aumentado el acoplamiento entre los módulos del Honeypot y el IPS. |
| **Herencia Simple para el IPS** | Crear subclases completas como `MotorIPSWindows` y `MotorIPSLinux` habría provocado una duplicación innecesaria del código del bucle principal de consultas a la base de datos. |
| **Variables Globales Simples** | Aunque permiten compartir el estado de la conexión, no ofrecen un control seguro sobre el ciclo de vida de la misma (por ejemplo, reabrirla automáticamente si el servidor la cierra de forma inesperada). |

---

## Consecuencias

** Lo que gano:**

- **Técnica:** El sistema se vuelve altamente resiliente ante ráfagas de eventos de red y el motor IPS adquiere portabilidad total, facilitando su futuro despliegue en entornos Linux o contenedores.
- **Proceso:** Establece una convención clara en el equipo para agregar nuevos métodos de bloqueo en el futuro (ej. firewalls en la nube) simplemente creando una nueva clase de Estrategia, sin tocar el código central.

** Lo que sacrifico o asumo:**

- **Limitación técnica:** El patrón Singleton en Python requiere manejo cuidadoso en entornos altamente concurrentes; aunque la librería subyacente soporta los hilos actuales, escalar a multiprocesamiento severo podría requerir bloqueos mecánicos (locks).
- **Deuda o riesgo:** Se introduce una mayor abstracción y complejidad al código base mediante clases abstractas (`ABC`), lo que requerirá mayor documentación técnica para que otros desarrolladores comprendan el flujo de mitigación.

---

## Diagrama

Un boceto de cómo se estructura tu sistema (draw.io, Mermaid o a mano escaneado)

![Diagrama_Patrones](./ruta/diagrama_uml_patrones.png)

---

## Clausula de Uso de IA

Este documento fue redactado de forma personal. Se utilizó inteligencia artificial como herramienta de apoyo en los siguientes aspectos específicos:

| Área de uso | Descripción |
| --- | --- |
| **Consultoría Arquitectónica** | Se empleó la IA para determinar los patrones GOF más adecuados (Singleton y Strategy) basados en las vulnerabilidades operativas del código existente. |
| **Estructuración de Código Base** | Apoyo en la refactorización segura del bucle principal del IPS y la implementación de las clases abstractas en Python para el prototipo funcional. |