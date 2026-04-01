from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TenantCreate(BaseModel):
    company_name: str
    default_language: str = "es"


class LeadCreate(BaseModel):
    name: str
    contact: str
    source: str = "manual"


class MoveLeadStage(BaseModel):
    stage: str


class CampaignCreate(BaseModel):
    name: str
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
