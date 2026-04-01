import logging
import time
import uuid

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.core.config import settings
from app.db.base import Base
from app.db.models import Tenant, User
from app.db.session import AsyncSessionLocal, engine
from app.modules.ai.router import router as ai_router
from app.modules.analytics.router import router as analytics_router
from app.modules.automations.router import router as automations_router
from app.modules.calls.router import router as calls_router
from app.modules.campaigns.router import router as campaigns_router
from app.modules.leads.router import router as leads_router
from app.modules.tenants.router import router as tenants_router
from app.modules.users.router import router as users_router
from app.services.realtime import hub
from app.services.security import hash_password

app = FastAPI(title=settings.app_name)
logger = logging.getLogger("pam.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router)
app.include_router(tenants_router)
app.include_router(leads_router)
app.include_router(campaigns_router)
app.include_router(calls_router)
app.include_router(ai_router)
app.include_router(automations_router)
app.include_router(analytics_router)


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        tenant = await session.scalar(select(Tenant).where(Tenant.name == "PAM Demo"))
        if not tenant:
            tenant = Tenant(name="PAM Demo", default_language="es")
            session.add(tenant)
            await session.flush()
        admin = await session.scalar(select(User).where(User.email == "davidksinc@gmail.com"))
        if not admin:
            session.add(
                User(
                    email="davidksinc@gmail.com",
                    password_hash=hash_password("PamAdmin123!"),
                    tenant_id=tenant.id,
                    preferred_language="es",
                    is_super_admin=True,
                    is_active=True,
                )
            )
        await session.commit()


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("request_failed request_id=%s path=%s method=%s", request_id, request.url.path, request.method)
        return JSONResponse(status_code=500, content={"detail": "Error interno de servidor", "request_id": request_id})
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed request_id=%s method=%s path=%s status=%s elapsed_ms=%s",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.websocket("/ws/live/{tenant_id}")
async def live_updates(ws: WebSocket, tenant_id: int) -> None:
    channel = f"tenant:{tenant_id}"
    await hub.connect(channel, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(channel, ws)
