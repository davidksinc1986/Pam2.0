from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PAM AI Contact Center"
    environment: str = "dev"

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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
