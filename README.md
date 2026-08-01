# CRYSTAL - Ecosistema de Defensa Activa e Inteligente
**Arquitectura de Software - Actividad #40: Documentación final y demo**

##  Demo en Vivo y Pipeline CI
* **Demo funcional (Video):** [https://drive.google.com/file/d/1sjfeJDrBFRwm_O3jThgAXx2J969xCblO/view?usp=sharing]
* **Pipeline CI:** Implementado en GitHub Actions (Ver historial de commits / Actions). Se integró exitosamente validación y pruebas automatizadas (xUnit) sobre la API .NET.

---

##  Documentación Arquitectónica

### 1. Decisiones Arquitectónicas (ADR)
Todos los registros de decisiones (ADR) desde la Unidad II se encuentran actualizados en la carpeta `docs/adr-records` (o en la raíz del proyecto):
* ADR-05, ADR-06 (Patrones GoF) y ADR-07 (Deuda Técnica).

### 2. Modelo C4 (Niveles 1 al 3)
Los diagramas actualizados a la versión final del proyecto, incluyendo el Nivel 3 (Componentes), se encuentran en la carpeta `diagramas` y documentados en el historial de commits.

---

## 🛡️ Evaluación ATAM
Con base en la arquitectura asíncrona y el sensor DPI implementados, se identifican los siguientes puntos críticos:

* **Riesgo:** Cuello de botella en la Base de Datos. Si el sensor Honeypot (*Kalopsia*) recibe un ataque de denegación de servicio (DDoS) masivo, podría saturar las conexiones concurrentes a PostgreSQL.
* **Trade-off (Compromiso):** Bus de Eventos Asíncrono. Separar *Kalopsia* y el motor de bloqueo (*Paladin*) mediante PostgreSQL aumenta enormemente la resiliencia del sistema (si uno cae, el otro sigue operando), pero añade latencia a la respuesta en comparación con una ejecución directa en memoria.
* **Punto de Sensibilidad:** Consumo de CPU del motor DPI. La inspección profunda de paquetes es altamente sensible al volumen de tráfico anómalo, lo que puede degradar el rendimiento general del Host Windows protegido si no se implementan límites de tasa (rate limiting).

---

## 🤖 Declaración de Uso de IA
Se utilizó Inteligencia Artificial como apoyo en la optimización de algoritmos de red, diseño de la interfaz gráfica y configuración del pipeline CI/CD, siempre bajo la supervisión, estructuración y diseño arquitectónico estricto de mi autoría.