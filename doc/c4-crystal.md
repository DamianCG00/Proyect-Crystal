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