from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(32), index=True)
    external_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), default="")
    phone: Mapped[str] = mapped_column(String(64), default="")
    campaign_id: Mapped[str] = mapped_column(String(64), default="default")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
