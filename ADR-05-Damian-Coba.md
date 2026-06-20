# ADR-05: Implementación de Módulos Core y GUI en Python para el Ecosistema Crystal

| Campo | Valor |
|---|---|
| Autor | Damian Coba G. |
| Fecha | 19/06/2026 |
| Estado | `Aceptado` |

---

## Contexto

Como continuación al estilo de Arquitectura Orientada a Eventos definido previamente, se requiere construir los agentes locales del ecosistema **Crystal**: el Honeypot (Kalopsia), el motor IPS (Paladin) y la Interfaz Gráfica (GUI). El problema a resolver es encontrar una tecnología que permita implementar la concurrencia de estos módulos de forma rápida y efectiva para cumplir con el tiempo disponible de entrega del MVP, manteniendo la conexión con PostgreSQL como almacén de eventos.

---

## Decisión

Se decidió utilizar **Python** como lenguaje principal para el desarrollo de los módulos, empleando las librerías nativas `socket` y `threading` para la red y concurrencia, `psycopg2` para la base de datos, y `customtkinter` para la interfaz gráfica.

### ¿Por qué?

Python permite un *Rapid Prototyping* (prototipado rápido). La característica concreta que resuelve mi problema es su manejo nativo y simplificado de hilos (`threading`), lo que permite que Kalopsia escuche la red, Paladin consulte la base de datos y la GUI se actualice, todo de manera simultánea sin bloquear el hilo principal y logrando un producto funcional en tiempo récord.

### Alternativas consideradas

| Alternativa | Por qué la descarté |
|-------------|---------------------|
| **C# (.NET) para agentes locales** | Aunque la API del proyecto está en C#, forzar el desarrollo de scripts de red de bajo nivel y la GUI en este ecosistema habría incrementado drásticamente el tiempo de desarrollo. |
| **Node.js** | Aunque es excelente para asincronía, Python posee un ecosistema más maduro y directo para la interacción a bajo nivel con comandos del sistema operativo (como `netsh` para el firewall de Windows). |
| **C / C++** | Ofrece el mejor rendimiento para interacción con hardware y red, pero la gestión manual de memoria y el tiempo de compilación hacen inviable su uso para un MVP contra reloj. |

---

## Consecuencias

**✅ Lo que gano:**

- **Técnica:** Se vuelve sumamente fácil y rápido construir el manejo de sockets de red y la conexión a la base de datos con pocas líneas de código.
- **Proceso:** Acelera drásticamente la capacidad de iteración y pruebas del MVP por parte del equipo, permitiendo cumplir con la entrega a tiempo.

**⚠️ Lo que sacrifico o asumo:**

- **Limitación técnica:** El *Global Interpreter Lock* (GIL) de Python impide un paralelismo real multi-núcleo en CPU, aunque para las tareas limitadas por I/O (red y base de datos) de este MVP es suficiente.
- **Deuda o riesgo:** Tendré que gestionar la instalación manual de dependencias (`pip install`) en los equipos host antes de poder empaquetar el sistema en un ejecutable `.exe` final.

## Diagrama

Un boceto de cómo se estructura tu sistema (draw.io, Mermaid o a mano escaneado)

<img width="1084" height="229" alt="image" src="https://github.com/user-attachments/assets/cd7f577e-d2c8-47dd-b737-43c2606f1c0a" />

---

## Clausula de Uso de IA

Este documento fue redactado de forma personal. Se utilizó inteligencia artificial como herramienta de apoyo en los siguientes aspectos específicos:

| Área de uso | Descripción |
| --- | --- |
| **Estructuración de Código Base** | Se empleó la IA para generar el *boilerplate* de la conexión a PostgreSQL, el socket del Honeypot y la ventana de CustomTkinter, acelerando la creación del MVP. |
| **Resolución de Errores** | Apoyo técnico en la depuración de credenciales y roles de PostgreSQL (Error de Autenticación FATAL) en tiempo real. |
