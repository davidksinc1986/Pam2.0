# Análisis de fusión (PAM + leadgen-saas + coldcaller)

Se diseñó una arquitectura objetivo de microservicios para consolidar capacidades:

- Canal de voz (Twilio + FastAPI).
- Guionado de llamadas en tiempo real (WebSockets + FastAPI).
- Captura y persistencia de leads sociales (Meta webhook + PostgreSQL).
- Dashboard único para operación (React + TypeScript).

> Nota: la base actual entrega una implementación inicial funcional (MVP técnico) lista para ampliar en un repositorio llamado `PAM-CallLeadCenter`.
