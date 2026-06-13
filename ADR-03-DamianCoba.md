
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

## Alternativas consideradas

| Alternativa | Por qué la descarté |
| --- | --- |
| **Arquitectura en Capas / Clean Architecture (Propuesta tradicional)** | Se descartó porque Crystal no es un sistema CRUD financiero lineal. Separar el código en Domain, Application e Infrastructure añade capas de abstracción innecesarias para un software reactivo que responde directamente a estímulos asíncronos del hardware y de la red. |
| **Monolito Secuencial Síncrono (Llamadas directas)** | Implicaría que Kalopsia llamara directamente a las funciones de Paladin al detectar un ataque. Fue descartada porque congelaría los hilos de red; mientras el firewall aplica el bloqueo, el sistema dejaría de escuchar, abriendo una ventana de vulnerabilidad. |
| **Arquitectura de Microservicios (Contenedores)** | Separar el Honeypot, el IPS y la GUI en servicios independientes (ej. Docker). Se descartó porque rompería el requisito de portabilidad comercial. Exigir la instalación previa de Docker en un entorno host Windows corporativo añade una complejidad operativa inaceptable. |
| **Arquitectura Hexagonal completa (Ports & Adapters)** | Ofrece un gran aislamiento del núcleo de seguridad, pero requiere definir puertos de entrada y salida explícitos para cada componente. Para el alcance y tiempo de desarrollo de mi MVP, esto representa sobreingeniería. |

---

## Consecuencias

### Lo que gano:

Procesamiento de amenazas asíncrono y altamente tolerante a ráfagas de ataques concurrentes

Aislamiento total entre la detección (Honeypot/FIM), la mitigación (IPS) y la capa visual (GUI)

Escalabilidad simplificada: puedo añadir un nuevo consumidor de eventos (como un módulo de alerta por correo) simplemente haciéndolo leer la tabla de PostgreSQL, sin tocar el código de Kalopsia

 ### Lo que sacrifico o asumo:

Consistencia eventual: Existe una latencia entre el momento en que se inserta el evento de ataque y el instante en que Paladin ejecuta el bloqueo en el firewall

Complejidad en la depuración (Debugging), ya que el flujo de ejecución no es lineal y requiere auditar los timestamps guardados en la base de datos



---
## Diagrama

Un boceto de cómo se estructura tu sistema (draw.io, Mermaid o a mano escaneado)

![Diagrama del sistema]( ./ruta/diagrama-nivel-1.png )
