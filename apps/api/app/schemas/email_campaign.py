import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmailCampaignOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tipo: str
    assunto: str
    corpo_html: str
    corpo_texto: str
    status: str
    criado_em: datetime
    aprovado_em: datetime | None
    enviado_em: datetime | None


class EmailCampaignUpdate(BaseModel):
    assunto: str | None = None
    corpo_html: str | None = None
    corpo_texto: str | None = None
    status: str | None = None
