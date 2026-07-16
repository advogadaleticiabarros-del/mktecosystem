import uuid
from datetime import datetime

from pydantic import BaseModel


class GerarRequest(BaseModel):
    pauta_id: uuid.UUID


class ContentPieceOut(BaseModel):
    id: uuid.UUID
    pauta_id: uuid.UUID
    tipo: str
    corpo: dict
    status: str
    versao: int
    criado_em: datetime

    model_config = {"from_attributes": True}


class ContentPieceUpdate(BaseModel):
    corpo: dict | None = None
    status: str | None = None
