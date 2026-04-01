from fastapi import APIRouter
from app.services.i18n import t

router = APIRouter(prefix="/ai", tags=["ai"])
memory: dict[int, dict] = {}


@router.post("/profile/{company_id}")
async def configure_ai(company_id: int, payload: dict) -> dict:
    memory[company_id] = {
        "assistant_name": payload.get("assistant_name", "PAM"),
        "tone": payload.get("tone", "profesional y cálido"),
        "language": payload.get("language", "es"),
        "behavior": payload.get("behavior", "resolver rápido y agendar seguimiento"),
        "faq": payload.get("faq", []),
    }
    return {"status": "configured", "ai": memory[company_id]}


@router.get("/memory/{company_id}")
async def get_memory(company_id: int) -> dict:
    return memory.get(company_id, {})


@router.get("/translate/{lang}/{key}")
async def translate(lang: str, key: str) -> dict:
    return {"lang": lang, "key": key, "text": t(lang, key)}
