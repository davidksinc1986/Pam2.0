# PAM AI Contact Center

Suite unificada SaaS multi-empresa para operación comercial:

- Recepción de llamadas entrantes con IA.
- Campañas salientes (agente asistido o IA automática).
- Gestión de contactos (social + manual).
- Pipeline CRM visual.
- Automatizaciones: WhatsApp + email follow-up.
- Lead scoring por IA (heurística extensible).
- Dashboard de analytics.
- Multi-language real (es/en/pt base).

---

## 1) Requisitos

- Docker + Docker Compose
- (Opcional) Python 3.11 para ejecutar scripts localmente

---

## 2) Configuración inicial

```bash
cp .env.example .env
```

Si no tienes credenciales externas, el sistema corre en **modo simulado** para WhatsApp/voz/email.

---

## 3) Levantar todo con Docker Compose

```bash
docker compose up --build
```

Servicios:

- API: http://localhost:8000/docs
- Frontend: http://localhost:5173
- Mailhog UI (emails): http://localhost:8025
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## 4) Inicializar datos (scripts de inicialización)

Con contenedores levantados:

```bash
docker compose exec api python scripts/init_db.py
```

O todo en un comando:

```bash
./scripts/bootstrap.sh
```

Esto crea:

- Empresa demo
- Super admin
- Leads y campaña de ejemplo

Credenciales iniciales:

- `davidksinc@gmail.com`
- `PamAdmin123!`

---

## 5) Flujo funcional (paso a paso)

1. Login JWT en `POST /auth/login`.
2. Crear empresa en `POST /companies` (solo super admin).
3. Crear leads en `POST /leads`.
4. Crear campañas en `POST /campaigns`.
5. Simular llamada inbound en `POST /calls/inbound`.
6. Mover etapa CRM en `PATCH /leads/{lead_id}/stage`.
7. Ejecutar scoring en `POST /leads/score`.
8. Enviar WhatsApp en `POST /automations/whatsapp`.
9. Enviar follow-up email en `POST /automations/email`.
10. Consultar analytics en `GET /analytics/dashboard`.
11. Conectar realtime en `WS /ws/live/{tenant_id}`.

---

## 6) Módulos backend

```text
/app
  /core
  /modules
      /calls
      /campaigns
      /leads
      /ai
      /users
      /tenants
      /automations
      /analytics
  /services
  /integrations
  /schemas
  /db
```

---

## 7) Notas de producción

- JWT real activo.
- Separación por empresa (`tenant_id`) en endpoints de negocio.
- Fallback en integraciones externas para evitar errores 500.
- Logs simples en worker para trazabilidad.
