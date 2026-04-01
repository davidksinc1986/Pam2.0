from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Literal
import os

app = FastAPI(title="PAM Call Service")

TWILIO_TRANSFER_NUMBER = os.getenv("TWILIO_TRANSFER_NUMBER", "")


class CallDecisionRequest(BaseModel):
    from_number: str
    campaign_id: str | None = None
    preferred_flow: Literal["agent", "script", "auto"] = "auto"


class CallDecisionResponse(BaseModel):
    route: Literal["agent", "script"]
    reason: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "calls"}


@app.post("/api/calls/decision", response_model=CallDecisionResponse)
async def call_decision(payload: CallDecisionRequest) -> CallDecisionResponse:
    if payload.preferred_flow == "agent":
        return CallDecisionResponse(route="agent", reason="Agent requested by campaign")
    if payload.preferred_flow == "script":
        return CallDecisionResponse(route="script", reason="Automated script requested by campaign")
    route = "agent" if payload.from_number.endswith(("0", "2", "4", "6", "8")) else "script"
    return CallDecisionResponse(route=route, reason="Default parity-based routing")


@app.post("/twilio/inbound")
async def twilio_inbound(From: str = Form(...), CallSid: str = Form(...)) -> Response:  # noqa: N803
    route = "agent" if From.endswith(("0", "2", "4", "6", "8")) else "script"
    if route == "agent" and TWILIO_TRANSFER_NUMBER:
        xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
    <Say language=\"es-MX\">Te transferiremos con un agente.</Say>
    <Dial>{TWILIO_TRANSFER_NUMBER}</Dial>
</Response>"""
    else:
        xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
    <Say language=\"es-MX\">Bienvenido a PAM. Iniciaremos un flujo automatizado para la llamada {CallSid}.</Say>
</Response>"""
    return Response(content=xml, media_type="application/xml")


@app.post("/api/calls/transfer/{call_sid}")
async def transfer_call(call_sid: str) -> dict[str, str]:
    if not TWILIO_TRANSFER_NUMBER:
        raise HTTPException(status_code=400, detail="Set TWILIO_TRANSFER_NUMBER to enable transfer")
    return {"status": "queued", "call_sid": call_sid, "to": TWILIO_TRANSFER_NUMBER}
