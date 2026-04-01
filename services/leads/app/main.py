from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import os

from .db import SessionLocal, engine, Base
from .models import Lead

app = FastAPI(title="PAM Leads Service")
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "change-me")


class LeadIn(BaseModel):
    source: str
    external_id: str
    full_name: str
    email: str = ""
    phone: str = ""
    campaign_id: str = "default"


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "leads"}


@app.post("/api/leads")
async def create_lead(payload: LeadIn, db: AsyncSession = Depends(get_db)) -> dict[str, str | int]:
    exists = await db.scalar(select(Lead).where(Lead.external_id == payload.external_id))
    if exists:
        raise HTTPException(status_code=409, detail="Lead already exists")
    lead = Lead(**payload.model_dump())
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return {"status": "created", "id": lead.id}


@app.get("/api/leads")
async def list_leads(db: AsyncSession = Depends(get_db)) -> list[dict[str, str | int]]:
    rows = (await db.scalars(select(Lead).order_by(Lead.id.desc()))).all()
    return [
        {
            "id": row.id,
            "source": row.source,
            "external_id": row.external_id,
            "full_name": row.full_name,
            "email": row.email,
            "phone": row.phone,
            "campaign_id": row.campaign_id,
        }
        for row in rows
    ]


@app.get("/webhooks/meta")
async def verify_meta(request: Request) -> str:
    params = request.query_params
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    if token != VERIFY_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid verify token")
    return challenge or ""


@app.post("/webhooks/meta")
async def receive_meta(payload: dict, db: AsyncSession = Depends(get_db)) -> dict[str, int]:
    created = 0
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            lead_id = str(value.get("leadgen_id", ""))
            if not lead_id:
                continue
            exists = await db.scalar(select(Lead).where(Lead.external_id == lead_id))
            if exists:
                continue
            lead = Lead(
                source="meta",
                external_id=lead_id,
                full_name=value.get("full_name", "Unknown"),
                email=value.get("email", ""),
                phone=value.get("phone_number", ""),
                campaign_id=value.get("ad_id", "meta-campaign"),
            )
            db.add(lead)
            created += 1
    await db.commit()
    return {"created": created}
