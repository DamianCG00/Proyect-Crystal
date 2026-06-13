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

¿Qué decidiste? Sé específico: nombra la tecnología, el patrón o el estilo arquitectónico que elegiste.

### ¿Por qué?

Argumenta tu decisión. No basta con decir "es lo que vimos en clase" — explica qué característica concreta de lo que elegiste resuelve tu problema.

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
