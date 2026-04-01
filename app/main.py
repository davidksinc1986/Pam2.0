from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                )
            )
        await session.commit()


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
