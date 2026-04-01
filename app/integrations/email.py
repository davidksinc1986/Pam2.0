import smtplib
from email.message import EmailMessage
from app.core.config import settings


async def send_followup_email(to_email: str, subject: str, body: str) -> dict:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=5) as server:
            server.send_message(msg)
        return {"status": "sent", "to": to_email}
    except OSError:
        return {"status": "simulated", "to": to_email, "reason": "smtp_unreachable"}
