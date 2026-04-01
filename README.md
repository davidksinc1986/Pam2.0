# PAM-CallLeadCenter

Arquitectura de fusión para PAM + LeadGen + ColdCaller, separada en microservicios:

- `services/calls`: recepción y decisión de enrutamiento de llamadas (Twilio).
- `services/callcoaching`: guía de agentes en tiempo real via WebSockets.
- `services/leads`: captura de leads de Facebook/Instagram con webhook y persistencia en PostgreSQL.
- `frontend`: dashboard React + TypeScript con onboarding y tooltips.

## 1) Crear repositorio objetivo

Nombre sugerido: **PAM-CallLeadCenter**.

```bash
git init PAM-CallLeadCenter
```

## 2) Levantar plataforma completa

```bash
cp .env.example .env
docker compose up --build
```

Servicios:

- Frontend: `http://localhost:5173`
- Calls API: `http://localhost:8001/docs`
- Call-Coaching API/WS: `http://localhost:8002/docs`
- Leads API: `http://localhost:8003/docs`

## 3) Configurar credenciales

### Twilio

Configura en `.env`:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TWILIO_TRANSFER_NUMBER`

Luego apunta el webhook de voz de Twilio a:

- `POST /twilio/inbound` en `calls-service`

### Facebook / Instagram (Meta)

Configura en `.env`:

- `META_VERIFY_TOKEN`
- `META_APP_ID`
- `META_APP_SECRET`
- `META_ACCESS_TOKEN`

Registra webhook:

- Verificación: `GET /webhooks/meta`
- Eventos: `POST /webhooks/meta`

## 4) Flujo operativo

1. Entra una llamada por Twilio.
2. `calls-service` decide: agente o script automático.
3. Agente abre dashboard React y usa acciones de llamada.
4. Si usa guion, `callcoaching-service` guía paso a paso por WebSocket.
5. Leads de Meta se guardan en PostgreSQL y aparecen en dashboard.

## 5) Próximas expansiones recomendadas

- Orquestación central (API Gateway + Auth).
- Motor de reglas por campaña (score, horarios, disponibilidad).
- ETL de leads con normalización y deduplicación avanzada.
- Multi-tenant con RBAC y auditoría.

## 6) Guía de ejecución profesional

Para implementar cambios con foco en estabilidad, UX para usuarios no técnicos y salida a producción, sigue la guía:

- `docs/principios-plataforma-saas.md`
