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
