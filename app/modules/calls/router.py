from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_current_user, get_db
from app.db.models import Call, User
from app.services.realtime import hub

router = APIRouter(prefix="/calls", tags=["calls"])


@router.post("/inbound")
async def inbound_call(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    payload = await request.json()
    tenant_id = int(payload.get("tenant_id", 1))
    call = Call(tenant_id=tenant_id, direction="inbound", status="answered", transcript="Llamada entrante iniciada")
    db.add(call)
    await db.commit()
    await db.refresh(call)
    await hub.publish(f"tenant:{tenant_id}", {"type": "call_live", "call_id": call.id, "status": call.status})
    return {"id": call.id, "status": call.status, "transfer_available": True}


@router.post("/outbound")
async def outbound_call(payload: dict, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    call = Call(tenant_id=user.tenant_id, direction="outbound", status="answered", transcript=payload.get("script", ""))
    db.add(call)
    await db.commit()
    await db.refresh(call)
    return {"id": call.id, "result": payload.get("result", "interested")}


@router.post("/{call_id}/transfer")
async def transfer_call(call_id: int, user: User = Depends(get_current_user)) -> dict:
    return {"id": call_id, "status": "transferred", "company_id": user.tenant_id}
