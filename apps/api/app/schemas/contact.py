import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ContactCreate(BaseModel):
    tenant_slug: str
    nome: str
    email: EmailStr
    origem: str = "lp"
    website: str = ""  # honeypot: humanos deixam vazio


class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: str
    origem: str
    status: str
    welcome_step: int
    criado_em: datetime
