from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.db.models import User
from app.schemas.common import LoginRequest, UserCreate, UserUpdate
from app.services.security import create_access_token, hash_password, verify_password

router = APIRouter(tags=["auth-users"])


@router.post("/auth/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> dict:
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario desactivado")
    token = create_access_token(user.email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "is_super_admin": user.is_super_admin,
            "is_active": user.is_active,
        },
    }


@router.get("/auth/me")
async def me(user: User = Depends(get_current_user)) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "preferred_language": user.preferred_language,
        "is_super_admin": user.is_super_admin,
        "is_active": user.is_active,
    }


@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[dict]:
    rows = (
        await db.scalars(
            select(User).where(User.tenant_id == current_user.tenant_id).order_by(User.id.desc())
        )
    ).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "tenant_id": user.tenant_id,
            "preferred_language": user.preferred_language,
            "is_super_admin": user.is_super_admin,
            "is_active": user.is_active,
        }
        for user in rows
    ]


@router.post("/users")
async def create_user(
    payload: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> dict:
    target_tenant = payload.tenant_id if current_user.is_super_admin and payload.tenant_id else current_user.tenant_id
    if payload.tenant_id and payload.tenant_id != current_user.tenant_id and not current_user.is_super_admin:
        raise HTTPException(status_code=403, detail="No tienes permisos para crear usuarios en otra empresa")
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        tenant_id=target_tenant,
        preferred_language=payload.preferred_language,
        is_super_admin=bool(payload.is_super_admin and current_user.is_super_admin),
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="El email ya existe") from exc
    await db.refresh(user)
    return {"id": user.id, "email": user.email, "tenant_id": user.tenant_id, "is_active": user.is_active}


@router.patch("/users/{user_id}")
async def update_user(
    user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> dict:
    user = await db.scalar(select(User).where(User.id == user_id, User.tenant_id == current_user.tenant_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if payload.preferred_language is not None:
        user.preferred_language = payload.preferred_language
    if payload.is_active is not None:
        if user.id == current_user.id and payload.is_active is False:
            raise HTTPException(status_code=400, detail="No puedes desactivar tu propio usuario")
        user.is_active = payload.is_active
    await db.commit()
    return {"id": user.id, "preferred_language": user.preferred_language, "is_active": user.is_active}
