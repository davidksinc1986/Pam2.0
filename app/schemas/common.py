from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TenantCreate(BaseModel):
    company_name: str
    default_language: str = "es"


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    contact: str = Field(min_length=3, max_length=120)
    source: str = "manual"


class MoveLeadStage(BaseModel):
    stage: str


class CampaignCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    mode: str = "assisted"
    script: str = ""
    language: str = "es"


class MessageCreate(BaseModel):
    lead_id: int | None = None
    content: str
    language: str = "es"


class ScoreRequest(BaseModel):
    lead_id: int
    interaction_summary: str = ""


class OnboardingUpdate(BaseModel):
    onboarding_step: int = Field(ge=1, le=4)
    ai_assistant_name: str = Field(min_length=2, max_length=80)
    ai_tone: str = Field(min_length=2, max_length=120)
    ai_behavior: str = Field(min_length=5)
    playbook: str = ""
