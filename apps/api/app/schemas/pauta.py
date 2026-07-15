import uuid
from datetime import datetime

from pydantic import BaseModel


class PautaOut(BaseModel):
    id: uuid.UUID
    titulo: str
    angulo: str
    area: str
    origem: str
    fonte: str
    relevante_para_conteudo: bool
    status: str
    criado_em: datetime

    model_config = {"from_attributes": True}


class PautaManualCreate(BaseModel):
    titulo: str
    angulo: str
    area: str
