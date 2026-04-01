from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.db.models import Tenant, User
from app.schemas.common import TenantCreate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("")
async def create_company(payload: TenantCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    if not user.is_super_admin:
        raise HTTPException(status_code=403, detail="Solo super admin puede crear empresas")
    tenant = Tenant(name=payload.company_name, default_language=payload.default_language)
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    return {"id": tenant.id, "company_name": tenant.name, "default_language": tenant.default_language}


@router.get("/me")
async def my_company(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    tenant = await db.scalar(select(Tenant).where(Tenant.id == user.tenant_id))
    return {"id": tenant.id, "company_name": tenant.name, "default_language": tenant.default_language}
