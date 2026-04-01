from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        email = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Token inválido") from exc
    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
