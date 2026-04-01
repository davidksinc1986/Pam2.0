from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db
from app.db.models import User
from app.schemas.common import LoginRequest
from app.services.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> dict:
    user = await db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer", "user": {"email": user.email, "tenant_id": user.tenant_id}}
