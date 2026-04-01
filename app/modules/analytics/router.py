from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.db.models import Call, Campaign, Lead, MessageLog, User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant_id = user.tenant_id
    leads_total = await db.scalar(select(func.count(Lead.id)).where(Lead.tenant_id == tenant_id))
    qualified = await db.scalar(select(func.count(Lead.id)).where(Lead.tenant_id == tenant_id, Lead.stage == "Qualified"))
    calls_total = await db.scalar(select(func.count(Call.id)).where(Call.tenant_id == tenant_id))
    campaigns_total = await db.scalar(select(func.count(Campaign.id)).where(Campaign.tenant_id == tenant_id))
    whatsapp_total = await db.scalar(select(func.count(MessageLog.id)).where(MessageLog.tenant_id == tenant_id, MessageLog.channel == "whatsapp"))
    email_total = await db.scalar(select(func.count(MessageLog.id)).where(MessageLog.tenant_id == tenant_id, MessageLog.channel == "email"))
    return {
        "leads_total": leads_total or 0,
        "qualified_total": qualified or 0,
        "calls_total": calls_total or 0,
        "campaigns_total": campaigns_total or 0,
        "whatsapp_messages": whatsapp_total or 0,
        "email_followups": email_total or 0,
    }
