from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "PAM AI Contact Center"
    environment: str = "dev"
    cors_origins: list[str] = ["http://localhost:5173"]

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 60 * 12

    database_url: str = "postgresql+asyncpg://pam:pam@db:5432/pam_ai_contact_center"
    redis_url: str = "redis://redis:6379/0"

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    whatsapp_phone_number: str = ""

    smtp_host: str = "mailhog"
    smtp_port: int = 1025
    smtp_from: str = "noreply@pam-ai.local"

    openai_api_key: str = ""
    deepgram_api_key: str = ""
    elevenlabs_api_key: str = ""

    bootstrap_admin_email: str = ""
    bootstrap_admin_password: str = ""

    @field_validator("jwt_secret")
    @classmethod
    def validate_jwt_secret(cls, value: str) -> str:
        if value in {"change-me", "super-change-me"}:
            raise ValueError("JWT_SECRET inseguro: configura un secreto real")
        return value


    @field_validator("bootstrap_admin_password")
    @classmethod
    def validate_bootstrap_admin_password(cls, value: str) -> str:
        if value and len(value) < 8:
            raise ValueError("BOOTSTRAP_ADMIN_PASSWORD debe tener al menos 8 caracteres")
        return value

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
