from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from collections import defaultdict

app = FastAPI(title="PAM Call-Coaching Service")

scripts: dict[str, list[str]] = defaultdict(list)


class ScriptPayload(BaseModel):
    campaign_id: str
    steps: list[str]


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "callcoaching"}


@app.post("/api/scripts")
async def load_script(payload: ScriptPayload) -> dict[str, str | int]:
    scripts[payload.campaign_id] = payload.steps
    return {"status": "loaded", "campaign_id": payload.campaign_id, "steps": len(payload.steps)}


@app.websocket("/ws/call-guide/{campaign_id}")
async def call_guide(websocket: WebSocket, campaign_id: str) -> None:
    await websocket.accept()
    campaign_steps = scripts.get(campaign_id, [])
    idx = 0
    try:
        await websocket.send_json({"type": "session_started", "campaign_id": campaign_id})
        while True:
            message = await websocket.receive_json()
            action = message.get("action")
            if action == "next":
                if idx < len(campaign_steps):
                    await websocket.send_json({"type": "step", "index": idx, "text": campaign_steps[idx]})
                    idx += 1
                else:
                    await websocket.send_json({"type": "done", "message": "Script completed"})
            elif action == "response":
                await websocket.send_json({"type": "ack", "saved": True, "payload": message.get("payload", {})})
            else:
                await websocket.send_json({"type": "error", "message": "Unknown action"})
    except WebSocketDisconnect:
        return
