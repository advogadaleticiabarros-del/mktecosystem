import uuid
from datetime import date, datetime

from typing import Literal

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
    alerta_atualidade: str | None = None
    verificado_em: datetime | None = None
    conteudo_bruto: str | None = None
    data_editorial: date | None = None
    apuracao: dict | None = None
    relevancia: int | None = None
    urgencia: str | None = None
    criado_em: datetime

    model_config = {"from_attributes": True}


class PautaManualCreate(BaseModel):
    titulo: str
    angulo: str
    area: str
    origem: str = "manual"
    conteudo_bruto: str | None = None
    data_editorial: date | None = None


STATUS_PAUTA = Literal["sugerida", "aprovada", "em_producao", "publicada", "guardada", "descartada"]


class PautaStatusUpdate(BaseModel):
    status: STATUS_PAUTA


class PedidoJornalista(BaseModel):
    foco: str
