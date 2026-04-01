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

Si no tienes credenciales externas, los módulos dependientes (telefonía/WhatsApp/LLM) se muestran como **pendientes de configuración** y retornan error HTTP 412 donde aplique. No se finge ejecución exitosa.

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

- Empresa base `PAM Demo`
- Super admin inicial (idempotente)

Credenciales iniciales:

- Se crean de forma segura con variables de entorno `BOOTSTRAP_ADMIN_EMAIL` y `BOOTSTRAP_ADMIN_PASSWORD`.
- No se incluyen contraseñas hardcodeadas en el repositorio.

---

## 5) Flujo funcional (paso a paso)

1. Login JWT en `POST /auth/login`.
2. Crear empresa en `POST /companies` (solo super admin).
3. Crear usuarios de empresa en `POST /users`.
4. Crear leads en `POST /leads`.
5. Crear campañas en `POST /campaigns`.
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

- JWT real activo + estado de usuario (`is_active`).
- Separación por empresa (`tenant_id`) en endpoints de negocio.
- Integraciones externas no configuradas devuelven errores explícitos (sin mock silencioso).
- Logging estructurado básico con `X-Request-ID`.
