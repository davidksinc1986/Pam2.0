# Principios de implementación y operación SaaS (PAM 2.0)

Este documento define cómo evolucionar la plataforma sin romper funcionalidades existentes y con foco en salida a producción.

## 1) Principios no negociables

1. **No romper funcionalidades existentes**: todo cambio debe partir de pruebas de regresión mínimas de servicios impactados.
2. **Validar antes de cambiar**: inspeccionar contratos API, variables de entorno y dependencias antes de editar código.
3. **Explicar en comentarios**: cuando una decisión técnica no sea obvia, dejar comentario corto en el código o en PR.
4. **Diseñar para vender**: cada feature debe conectar con valor comercial, onboarding y métrica de conversión.
5. **Experiencia para no técnicos**: evitar términos internos en UI y priorizar acciones guiadas.

## 2) Checklist de diseño (antes de codificar)

- **Arquitectura**:
  - Servicio afectado (`calls`, `callcoaching`, `leads`, `frontend`).
  - Contratos de entrada/salida (HTTP/WS/webhooks).
  - Impacto en multi-tenant (aislamiento de datos y configuración).
- **Producto**:
  - Historia de usuario clara.
  - Métrica de éxito (ej: lead capturado, llamada transferida, tiempo de onboarding).
- **UX/UI**:
  - Flujo de 3 pasos máximo para tarea principal.
  - Texto orientado a acción y sin jerga técnica.
- **DevOps**:
  - Variables nuevas documentadas.
  - Compatibilidad con `docker compose up --build`.

## 3) Checklist de implementación

- Crear/actualizar modelos y esquemas sin romper contratos públicos existentes.
- Mantener endpoints compatibles o versionar cambios.
- Manejar errores con mensajes operativos y códigos HTTP consistentes.
- Añadir logs accionables para incidencias de producción.
- En cambios visuales relevantes, adjuntar screenshot de validación.

## 4) Checklist de validación (antes de merge)

- Salud de servicios (`/health` o arranque limpio).
- Flujos críticos:
  - Entrada de llamada Twilio.
  - Sesión de coaching por WebSocket.
  - Recepción de lead Meta y persistencia.
  - Visualización básica en dashboard.
- Verificación de migraciones/configuración en entorno local.
- Registro de riesgos residuales y plan de rollback.

## 5) Definición de “lista para vender”

Una entrega está lista para vender cuando cumple:

- Flujo end-to-end verificable (captura → gestión → seguimiento).
- Onboarding claro para usuario no técnico.
- Telemetría mínima operativa (errores, latencia, conversiones).
- Despliegue reproducible en VM con documentación actualizada.
