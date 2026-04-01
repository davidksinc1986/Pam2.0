from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.db.models import Campaign, User
from app.schemas.common import CampaignCreate

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("")
async def create_campaign(payload: CampaignCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    campaign = Campaign(tenant_id=user.tenant_id, name=payload.name, mode=payload.mode, script=payload.script, language=payload.language)
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return {"id": campaign.id, "name": campaign.name, "language": campaign.language}


@router.get("")
async def list_campaigns(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    rows = (await db.scalars(select(Campaign).where(Campaign.tenant_id == user.tenant_id).order_by(Campaign.id.desc()))).all()
    return [{"id": x.id, "name": x.name, "mode": x.mode, "script": x.script, "language": x.language} for x in rows]


@router.put("/{campaign_id}")
async def update_campaign(campaign_id: int, payload: CampaignCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    campaign = await db.scalar(select(Campaign).where(Campaign.id == campaign_id, Campaign.tenant_id == user.tenant_id))
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaña no encontrada")
    campaign.name = payload.name
    campaign.mode = payload.mode
    campaign.script = payload.script
    campaign.language = payload.language
    await db.commit()
    return {"id": campaign.id, "name": campaign.name, "mode": campaign.mode, "script": campaign.script, "language": campaign.language}
