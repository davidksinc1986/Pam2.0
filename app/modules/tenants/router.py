from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.db.models import Tenant, User
from app.schemas.common import OnboardingUpdate, TenantCreate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("")
async def create_company(payload: TenantCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    if not user.is_super_admin:
        raise HTTPException(status_code=403, detail="Solo super admin puede crear empresas")
    tenant = Tenant(name=payload.company_name, default_language=payload.default_language)
    db.add(tenant)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="La empresa ya existe") from exc
    await db.refresh(tenant)
    return {
        "id": tenant.id,
        "company_name": tenant.name,
        "default_language": tenant.default_language,
    }


@router.get("")
async def list_companies(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    if not user.is_super_admin:
        raise HTTPException(status_code=403, detail="Solo super admin puede consultar empresas")
    rows = (await db.scalars(select(Tenant).order_by(Tenant.id.desc()))).all()
    return [{"id": row.id, "company_name": row.name, "default_language": row.default_language} for row in rows]


@router.get("/me")
async def my_company(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id))
    return {
        "id": tenant.id,
        "company_name": tenant.name,
        "default_language": tenant.default_language,
        "onboarding_step": tenant.onboarding_step,
        "ai_assistant_name": tenant.ai_assistant_name,
        "ai_tone": tenant.ai_tone,
        "ai_behavior": tenant.ai_behavior,
        "playbook": tenant.playbook,
    }


@router.put("/me/onboarding")
async def update_onboarding(payload: OnboardingUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id))
    tenant.onboarding_step = payload.onboarding_step
    tenant.ai_assistant_name = payload.ai_assistant_name
    tenant.ai_tone = payload.ai_tone
    tenant.ai_behavior = payload.ai_behavior
    tenant.playbook = payload.playbook
    await db.commit()
    return {"status": "saved", "onboarding_step": tenant.onboarding_step}
