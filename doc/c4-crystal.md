# Arquitectura C4 - Ecosistema de Ciberseguridad Crystal

## C4 Nivel 1 - Contexto
**Para quién es:** Para cualquier persona interesada en la seguridad del sistema, incluyendo usuarios finales, administradores y profesores evaluadores.
**Qué pregunta responde:** ¿Qué es el ecosistema Crystal y quién interactúa con él a gran escala?

```mermaid
graph TD
    Admin[Administrador de Seguridad] -->|Monitorea y gestiona alertas| Crystal[Ecosistema Crystal]
    Atacante[Tráfico de Red / Posible Atacante] -.->|Intenta acceder| Red[Infraestructura de Red]
    
    Red -->|Redirige tráfico sospechoso| Crystal
    Crystal -->|Bloquea amenazas| Red
```

---

## C4 Nivel 2 - Contenedores
**Para quién es:** Para el equipo de desarrollo técnico y evaluadores de arquitectura.
**Qué pregunta responde:** ¿Cuáles son los contenedores principales del ecosistema Crystal (módulo sensor, actuador, API, base de datos) y cómo se comunican entre sí?

```mermaid
graph TD
    Admin[Administrador] -->|Usa Interfaz Gráfica| GUI[Crystal GUI: Python]
    Atacante[Tráfico de Red] -.->|Intenta conexión| Sensor[Kalopsia: Servidor Honeypot]
    
    GUI -->|Consulta alertas| API[Crystal API: .NET Core]
    Sensor -->|Envía datos de amenaza| API
    
    API -->|Registra eventos| DB[(Base de Datos: PostgreSQL)]
    API -->|Notifica bloqueo| Actuador[Paladín: Motor IPS]
    
    Actuador -->|Aplica reglas de bloqueo| OS[Sistema Operativo / Firewall]
```

---


## C4 Nivel 3 - Componentes
**Para quién es:** Para los desarrolladores encargados del mantenimiento, blindaje y mejora del código.
**Qué pregunta responde:** ¿Qué hay dentro de las piezas principales de Crystal y cómo se implementan los patrones de diseño y las medidas de seguridad internas?

```mermaid
graph TD
    %% Módulo Sensor Kalopsia
    subgraph Kalopsia [Módulo Sensor: Kalopsia]
        Honeypot[Honeypot Server] --> Logger[Servicio de Logging Seguro]
        Logger -->|Envía alerta vía HTTP POST| ApiCtrl[AlertasController]
    end
    
    %% API y Lógica de Negocio
    subgraph Crystal_API [Crystal API - ASP.NET Core]
        ApiCtrl --> SecService[Servicio de Análisis de Ciberseguridad]
        
        %% Patrones y Blindaje
        SecService -->|Patrón Strategy| Mitigacion[Estrategias de Mitigación]
        SecService -->|Blindaje y Validación| Validador[Módulo de Validación de Entrada]
    end
    
    %% Módulo Actuador Paladín y Base de Datos
    subgraph Core_Backend [Infraestructura y Actuadores]
        Mitigacion -->|Ejecuta comandos| Bloqueador[Paladín: IPS Blocker]
        Validador -->|Transacciones Seguras| PgConnection[conexion_pg.py: Singleton]
    end
```

---

## Declaración de Uso de IA
Esta documentación ha sido elaborada de manera autónoma, basando la estructura arquitectónica y el diseño de componentes íntegramente en el código fuente de mi autoría (Ecosistema Crystal). Se empleó asistencia de inteligencia artificial (Gemini) de manera exclusiva para la generación técnica de la sintaxis y el renderizado gráfico de los diagramas Mermaid presentados en este documento.