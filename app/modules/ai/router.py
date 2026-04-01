from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.db.models import Tenant, User
from app.services.i18n import t

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/profile")
async def configure_ai(payload: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id))
    tenant.ai_assistant_name = payload.get("assistant_name", tenant.ai_assistant_name)
    tenant.ai_tone = payload.get("tone", tenant.ai_tone)
    tenant.ai_behavior = payload.get("behavior", tenant.ai_behavior)
    await db.commit()
    return {
        "status": "configured",
        "ai": {
            "assistant_name": tenant.ai_assistant_name,
            "tone": tenant.ai_tone,
            "language": tenant.default_language,
            "behavior": tenant.ai_behavior,
        },
    }


@router.get("/memory")
async def get_memory(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id))
    return {
        "assistant_name": tenant.ai_assistant_name,
        "tone": tenant.ai_tone,
        "language": tenant.default_language,
        "behavior": tenant.ai_behavior,
        "playbook": tenant.playbook,
    }


@router.get("/translate/{lang}/{key}")
async def translate(lang: str, key: str) -> dict:
    return {"lang": lang, "key": key, "text": t(lang, key)}
