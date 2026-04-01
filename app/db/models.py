from sqlalchemy import String, ForeignKey, DateTime, Text, Boolean, Integer, func, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    default_language: Mapped[str] = mapped_column(String(10), default="es")
    onboarding_step: Mapped[int] = mapped_column(Integer, default=1)
    ai_assistant_name: Mapped[str] = mapped_column(String(80), default="PAM")
    ai_tone: Mapped[str] = mapped_column(String(120), default="profesional y cálido")
    ai_behavior: Mapped[str] = mapped_column(Text, default="resolver rápido y agendar seguimiento")
    playbook: Mapped[str] = mapped_column(Text, default="")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="es")
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    contact: Mapped[str] = mapped_column(String(120))
    source: Mapped[str] = mapped_column(String(80), default="manual")
    stage: Mapped[str] = mapped_column(String(40), default="New")
    score: Mapped[float] = mapped_column(Float, default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Campaign(Base):
    __tablename__ = "campaigns"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    mode: Mapped[str] = mapped_column(String(40), default="assisted")
    script: Mapped[str] = mapped_column(Text, default="")
    language: Mapped[str] = mapped_column(String(10), default="es")


class Call(Base):
    __tablename__ = "calls"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id"), nullable=True)
    direction: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(40), default="answered")
    transcript: Mapped[str] = mapped_column(Text, default="")
    recording_url: Mapped[str] = mapped_column(String(255), default="")
    duration_sec: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class MessageLog(Base):
    __tablename__ = "message_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id"), nullable=True)
    channel: Mapped[str] = mapped_column(String(30))
    direction: Mapped[str] = mapped_column(String(20), default="outbound")
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="queued")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
