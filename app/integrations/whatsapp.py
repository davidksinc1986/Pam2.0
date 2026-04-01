from app.core.config import settings


async def send_whatsapp(to_number: str, message: str) -> dict:
    # Fallback local mode (without external provider)
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        return {"status": "simulated", "to": to_number, "provider": "local-fallback", "message": message}
    return {"status": "queued", "to": to_number, "provider": "twilio", "message": message}
