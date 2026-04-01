from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://pam:pam@postgres:5432/pam_callleadcenter"
)

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
