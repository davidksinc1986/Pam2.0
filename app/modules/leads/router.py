from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.db.models import Lead, User
from app.schemas.common import LeadCreate, MoveLeadStage, ScoreRequest
from app.services.lead_scoring import score_lead
from app.services.realtime import hub

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("")
async def create_lead(payload: LeadCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    lead = Lead(tenant_id=user.tenant_id, name=payload.name, contact=payload.contact, source=payload.source)
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    await hub.publish(f"tenant:{user.tenant_id}", {"type": "lead_created", "lead_id": lead.id, "name": lead.name})
    return {"id": lead.id, "stage": lead.stage, "score": lead.score}


@router.get("")
async def list_leads(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    rows = (await db.scalars(select(Lead).where(Lead.tenant_id == user.tenant_id).order_by(Lead.id.desc()))).all()
    return [{"id": x.id, "name": x.name, "contact": x.contact, "source": x.source, "stage": x.stage, "score": x.score, "notes": x.notes} for x in rows]


@router.put("/{lead_id}")
async def update_lead(lead_id: int, payload: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    lead = await db.scalar(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == user.tenant_id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    lead.name = payload.get("name", lead.name)
    lead.contact = payload.get("contact", lead.contact)
    lead.notes = payload.get("notes", lead.notes)
    await db.commit()
    return {"id": lead.id, "name": lead.name, "contact": lead.contact, "notes": lead.notes}


@router.patch("/{lead_id}/stage")
async def update_stage(lead_id: int, payload: MoveLeadStage, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    lead = await db.scalar(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == user.tenant_id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    lead.stage = payload.stage
    await db.commit()
    await hub.publish(f"tenant:{user.tenant_id}", {"type": "lead_moved", "lead_id": lead.id, "stage": lead.stage})
    return {"id": lead.id, "stage": lead.stage}


@router.post("/score")
async def score(payload: ScoreRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    lead = await db.scalar(select(Lead).where(Lead.id == payload.lead_id, Lead.tenant_id == user.tenant_id))
    if not lead:
        raise HTTPException(status_code=404, detail="Lead no encontrado")
    lead.score = score_lead(lead.source, lead.stage, payload.interaction_summary)
    await db.commit()
    return {"lead_id": lead.id, "score": lead.score}
