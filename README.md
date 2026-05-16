# ADR-01: Arquitectura Modular y Selección de Tecnologías para el Ecosistema de Defensa Activa "Crystal"

| Campo  | Valor |
|--------|-------|
| Autor  | Marco Damián |
| Fecha  | 15/05/2026 |
| Estado | `A la espera` |

---

## Contexto

Se está construyendo **"Crystal"**, un ecosistema de ciberseguridad enfocado en la Defensa Activa y la Monitorización de Integridad de Archivos (FIM). El proyecto resuelve la vulnerabilidad crítica de los sistemas de seguridad tradicionales que son puramente estáticos y reactivos, los cuales se limitan a esperar un incidente para actuar. Este software va dirigido a personas u organizaciones que requieren una infraestructura de seguridad adaptable y dinámica frente a amenazas continuas en sus estaciones de trabajo.

Las condiciones y restricciones clave que influyen en esta decisión arquitectónica incluyen la necesidad de asegurar portabilidad y compatibilidad comercial directa (razón por la cual se desarrolla sobre el sistema operativo Windows utilizando Visual Studio Community), el requisito de entregar un Producto Mínimo Viable (MVP) funcional en plazos académicos estrictos, y el aprovechamiento del dominio previo en programación orientada a objetos y lenguajes de alto nivel para acelerar el despliegue del software.

---

## Decisión

Se determinó diseñar e implementar una **Arquitectura Modular Desacoplada** dividida en componentes independientes de software, seleccionando **Python** como lenguaje de programación principal, **CustomTkinter** para el desarrollo de la interfaz gráfica de usuario (GUI) en modo oscuro moderno, y un modelo de comunicación interprocesos basado en **archivos estructurados JSON cifrados**.

El ecosistema se dividirá estrictamente en dos submódulos centrales: 
1. **Kalopsia:** Funciona de manera interna como un Honeypot pasivo (señuelo) y monitor FIM, encargado de recolectar Indicadores de Compromiso (IoCs).
2. **Paladin:** Funciona como un Sistema de Prevención de Intrusiones (IPS) local que interactúa directamente con las reglas de red del sistema operativo.

### ¿Por qué?

La selección de Python se fundamenta en su robustez nativa para la manipulación de redes, automatización de comandos del sistema y manejo de criptografía (librería `hashlib`). La separación en módulos independientes (Kalopsia y Paladin) mediante una arquitectura desacoplada resuelve el problema de disponibilidad y tolerancia a fallos: si el módulo de monitoreo o la interfaz visual sufren una interrupción o colapso, el escudo protector central (Paladin) puede seguir ejecutándose en segundo plano protegiendo el sistema operativo con las últimas directivas cargadas. 

Finalmente, la elección de CustomTkinter permite cumplir con la restricción estética y comercial, ofreciendo componentes visuales modernos y un acabado profesional sin la sobrecarga de dependencias de frameworks más masivos.

### Alternativas consideradas

| Alternativa | Por qué la descarté |
|-------------|---------------------|
| **Defensa Ofensiva (Hack-back)** | Se evaluó programar al módulo Kalopsia para rastrear y contraatacar activamente las fuentes de agresión de red. Se descartó por completo debido a las severas implicaciones éticas y legales (ilegalidad de accesos no autorizados de retorno), optando en su lugar por el aislamiento pasivo y bloqueo local. |
| **Desarrollo en Bash / Linux Puro** | Se contempló construir el ecosistema mediante scripts nativos de Bash para entornos GNU/Linux. Se descartó debido a que limitaba drásticamente la viabilidad comercial del producto en el mercado corporativo de escritorio (donde predomina Windows) y complicaba el empaquetado de una GUI avanzada. |
| **Tkinter Clásico** | Se analizó el uso de la librería gráfica estándar de Python para agilizar el desarrollo de la interfaz. Se descartó debido a su estética obsoleta y visualmente anticuada, lo cual disminuye la percepción de confiabilidad y el valor comercial de una herramienta de ciberseguridad. |

---

## Consecuencias

**✅ Lo que gano:**
- **Consecuencia técnica:** Alta escalabilidad y mantenibilidad. Al estar el núcleo lógico (Core), la interfaz (GUI) y las herramientas de voz aisladas en submódulos separados, es posible actualizar los algoritmos de hashing o los diccionarios de comandos de voz en el futuro sin riesgo de romper el sistema de bloqueo del Firewall o la renderización de las ventanas.
- **Consecuencia sobre el proceso o el equipo:** Permite un flujo de trabajo paralelo y limpio utilizando Git. Se facilita la creación de ramas (*branching*) independientes para trabajar en la interfaz gráfica o en el motor de red de forma atómica, reduciendo drásticamente la aparición de conflictos de código complejos (*merge conflicts*).

**⚠️ Lo que sacrifico o asumo:**
- **Limitación técnica:** Elevado consumo de recursos de hardware en el sistema host. La ejecución simultánea de un Honeypot de red, un monitor de integridad de archivos y un asistente de voz bidireccional exige el uso constante de hilos secundarios (`Threading`) en segundo plano, lo que impactará de forma directa en el uso de memoria RAM y ciclos de CPU.
- **Deuda o riesgo:** Riesgo operativo ante "Falsos Positivos". Si los criterios de detección en los archivos logs JSON no se calibran con extrema precisión, el componente Paladin podría interpretar tráfico de red legítimo o modificaciones automatizadas del sistema operativo como ataques críticos, inhabilitando puertos o servicios esenciales en el Firewall de Windows por error.
