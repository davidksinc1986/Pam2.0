from fastapi import APIRouter, Depends
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
    rows = (await db.scalars(select(Campaign).where(Campaign.tenant_id == user.tenant_id))).all()
    return [{"id": x.id, "name": x.name, "mode": x.mode, "script": x.script, "language": x.language} for x in rows]
