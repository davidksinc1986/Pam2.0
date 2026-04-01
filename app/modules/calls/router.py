from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.deps import get_current_user, get_db
from app.db.models import Call, User
from app.services.realtime import hub

router = APIRouter(prefix="/calls", tags=["calls"])


@router.get("")
async def list_calls(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    rows = (await db.scalars(select(Call).where(Call.tenant_id == user.tenant_id).order_by(Call.id.desc()))).all()
    return [{"id": x.id, "direction": x.direction, "status": x.status, "transcript": x.transcript, "duration_sec": x.duration_sec} for x in rows]


@router.post("/inbound")
async def inbound_call(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    payload = await request.json()
    tenant_id = int(payload.get("tenant_id", 1))
    call = Call(tenant_id=tenant_id, direction="inbound", status="answered", transcript="Llamada entrante iniciada")
    db.add(call)
    await db.commit()
    await db.refresh(call)
    await hub.publish(f"tenant:{tenant_id}", {"type": "call_live", "call_id": call.id, "status": call.status})
    return {"id": call.id, "status": call.status, "transfer_available": bool(settings.twilio_account_sid and settings.twilio_phone_number)}


@router.post("/outbound")
async def outbound_call(payload: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    if not settings.twilio_account_sid or not settings.twilio_phone_number:
        raise HTTPException(status_code=412, detail="Falta conectar Twilio para realizar llamadas salientes")
    call = Call(tenant_id=user.tenant_id, direction="outbound", status="answered", transcript=payload.get("script", ""), duration_sec=payload.get("duration_sec", 0))
    db.add(call)
    await db.commit()
    await db.refresh(call)
    return {"id": call.id, "result": payload.get("result", "completed")}


@router.post("/{call_id}/transfer")
async def transfer_call(call_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    call = await db.scalar(select(Call).where(Call.id == call_id, Call.tenant_id == user.tenant_id))
    if not call:
        raise HTTPException(status_code=404, detail="Llamada no encontrada")
    if not settings.twilio_account_sid or not settings.twilio_phone_number:
        raise HTTPException(status_code=412, detail="Falta conectar Twilio para transferir llamadas")
    call.status = "transferred"
    await db.commit()
    return {"id": call_id, "status": "transferred", "company_id": user.tenant_id}
