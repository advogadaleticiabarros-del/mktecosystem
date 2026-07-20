import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SocialConnectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    plataforma: str
    nome_conta: str
    status: str
    conectado_em: datetime
