# ADR-01: Arquitectura Modular y Selección de Tecnologías para el Ecosistema de Defensa Activa "Crystal"

| Campo  | Valor |
|--------|-------|
| Autor  | Marco Damián |
| Fecha  | 1/06/2026 |
| Estado | `Aprobada` |

---

## Contexto


En el ADR-02 se definió la transición de mi ecosistema **Crystal** hacia un modelo con almacenamiento relacional en PostgreSQL, gestionado en IntelliJ IDEA, permitiendo que los hilos de monitoreo escriban y consulten de forma concurrente.

Tras avanzar en el desarrollo, detecté la necesidad de formalizar el estilo arquitectónico del sistema, yendo más allá de la simple separación por hilos. El objetivo es definir cómo interactúan mis componentes de red y seguridad (Kalopsia y Paladin) con la base de datos y la interfaz gráfica, asegurando que el procesamiento masivo de alertas no congele la aplicación ni dismnuya el rendimiento del sistema operativo de Windows

Restricciones que se mantienen del ADR-02:

* **Concurrencia de datos:** Lecturas y escrituras simultáneas en tiempo real (IoCs de red y hashes FIM).
* **Tecnología:** Python, CustomTkinter, pgAdmin y PostgreSQL (sin cambios).
* **Portabilidad comercial:** El sistema completo debe ser capaz de empaquetarse en un único archivo ejecutable (`.exe`) para entornos corporativos Windows.


---
# ADR-01: Arquitectura Modular y Selección de Tecnologías para el Ecosistema de Defensa Activa "Crystal"

| Campo  | Valor |
|--------|-------|
| Autor  | Marco Damián |
| Fecha  | 12/06/2026 |
| Estado | `Aprobada` |

---

## Contexto


En el ADR-02 se definió la transición de mi ecosistema **Crystal** hacia un modelo con almacenamiento relacional en PostgreSQL, gestionado en IntelliJ IDEA, permitiendo que los hilos de monitoreo escriban y consulten de forma concurrente.

Tras avanzar en el desarrollo, detecté la necesidad de formalizar el estilo arquitectónico del sistema, yendo más allá de la simple separación por hilos. El objetivo es definir cómo interactúan mis componentes de red y seguridad (Kalopsia y Paladin) con la base de datos y la interfaz gráfica, asegurando que el procesamiento masivo de alertas no congele la aplicación ni dismnuya el rendimiento del sistema operativo de Windows

Restricciones que se mantienen del ADR-02:

* **Concurrencia de datos:** Lecturas y escrituras simultáneas en tiempo real (IoCs de red y hashes FIM).
* **Tecnología:** Python, CustomTkinter, pgAdmin y PostgreSQL (sin cambios).
* **Portabilidad comercial:** El sistema completo debe ser capaz de empaquetarse en un único archivo ejecutable (`.exe`) para entornos corporativos Windows.


---


## Decisión

Se adopta el estilo de **Arquitectura Orientada a Eventos (Event-Driven Architecture)**, implementado a través de un enfoque modular desacoplado temporalmente, donde PostgreSQL actúa como el canal central de comunicación (Event Store).

El sistema se organiza bajo una dinámica de productores y consumidores independientes:

1. **Productores de Eventos (Módulo Kalopsia):** Compuesto por hilos asíncronos dedicados. El hilo de red genera eventos cuando una IP interactúa con el puerto señuelo. El hilo FIM (vía watchdog) genera eventos ante modificaciones de hashes SHA-256 en el FileSystem.
2. **Almacén de Eventos (PostgreSQL):** Centraliza la inteligencia de amenazas en la tabla `eventos_amenaza`, actuando como el bus de datos inmutable que desacopla la detección de la respuesta.
3. **Consumidores de Eventos (Módulo Paladin e Interfaz GUI):** Paladin consume asíncronamente las alertas pendientes para inyectar bloqueos de red a nivel de sistema operativo (`netsh`). La interfaz CustomTkinter consume los datos de forma independiente para actualizar el visor de logs del operador.

---

## ¿Por qué este estilo resuelve mejor el problema?

* **Desacoplamiento temporal absoluto:** Kalopsia no necesita esperar a que el firewall aplique un bloqueo para seguir escuchando la red. Si el Honeypot recibe una ráfaga masiva de pings, los registra como eventos en milisegundos y continúa libre.
* **Resiliencia ante fallos del consumidor:** Si el módulo Paladin se detiene o el Firewall de Windows tarda en responder, los eventos se acumulan de forma segura en PostgreSQL. Ninguna alerta de intrusión se pierde en memoria RAM.
* **Mantenimiento de la UI Responsiva:** La interfaz gráfica (GUI) no procesa lógica de seguridad; actúa como un consumidor pasivo de eventos que se refresca sin interrumpir los hilos críticos de red.
* **Viabilidad del ejecutable único (.exe):** Al integrar la lógica de eventos dentro de los hilos de un mismo código Python, el sistema puede compilarse con PyInstaller sin depender de pesados orquestadores externos.

---

### Alternativas consideradas

*(Mínimo 3 filas)*

| Alternativa | Por qué la descarté |
|-------------|---------------------|
| ...         | ...                 |
| ...         | ...                 |
| ...         | ...                 |

---

## Consecuencias

**✅ Lo que gano:**

Menciona al menos:
- Una consecuencia **técnica** — qué se vuelve más fácil de construir, mantener o escalar en tu sistema
- Una consecuencia sobre el **proceso o el equipo** — cómo afecta la forma en que vas a trabajar

**⚠️ Lo que sacrifico o asumo:**

Menciona al menos:
- Una **limitación técnica** — qué no podrás hacer fácilmente con esta decisión
- Una **deuda o riesgo** — qué podrías tener que resolver más adelante si el proyecto crece

## Diagrama

Un boceto de cómo se estructura tu sistema (draw.io, Mermaid o a mano escaneado)

![Diagrama del sistema]( ./ruta/diagrama-nivel-1.png )
