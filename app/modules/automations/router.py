from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.db.models import Lead, MessageLog, User
from app.integrations.email import send_followup_email
from app.integrations.whatsapp import send_whatsapp
from app.schemas.common import MessageCreate

router = APIRouter(prefix="/automations", tags=["automations"])


@router.post("/whatsapp")
async def whatsapp_automation(payload: MessageCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    target = None
    if payload.lead_id:
        target = await db.scalar(select(Lead).where(Lead.id == payload.lead_id, Lead.tenant_id == user.tenant_id))
    to = target.contact if target else "unknown"
    result = await send_whatsapp(to, payload.content)
    db.add(MessageLog(tenant_id=user.tenant_id, lead_id=payload.lead_id, channel="whatsapp", content=payload.content, status=result["status"]))
    await db.commit()
    return result


@router.post("/email")
async def email_followup(payload: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    to_email = payload.get("to_email", "")
    subject = payload.get("subject", "Seguimiento PAM")
    body = payload.get("body", "Gracias por tu tiempo en la llamada.")
    result = await send_followup_email(to_email, subject, body)
    db.add(MessageLog(tenant_id=user.tenant_id, lead_id=payload.get("lead_id"), channel="email", content=body, status=result["status"]))
    await db.commit()
    return result
