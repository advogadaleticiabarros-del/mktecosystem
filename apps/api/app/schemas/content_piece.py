import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

# Convenção do campo `corpo` (JSON genérico, sem schema no banco) por tipo:
#   "carrossel": { "slides": [5 str], "imagens": [5 URLs], "legenda": str }
#   "pergunta":  { "pergunta": str, "imagem": URL, "legenda": str }
#   "frase":     { "frase": str (aceita <em>), "imagem": URL, "legenda": str }
#   "estatico":  { "conceito_visual": str, "texto_overlay": str, "imagem": URL, "legenda": str, "cta": str }
# "imagem"/"imagens" são opcionais: sem elas o publicador gera a arte (midia_instagram).
#   "stories":   { "roteiro": [3 str], "imagem": URL, "legenda": str }
#   "artigo":    { "titulo": str, "html": str, "meta_description": str, "resumo": str, "imagem_capa": URL }
#   "legenda":   { "texto": str }  (legado)
# URLs de imagem seguem o padrão {PUBLIC_API_URL}/media/{nome_arquivo}, servido por
# GET /media/{arquivo} e produzido por POST /media/upload.

TIPOS_CONTENT_PIECE = Literal["artigo", "carrossel", "legenda", "stories", "pergunta", "frase", "estatico"]


class GerarRequest(BaseModel):
    pauta_id: uuid.UUID


class ContentPieceOut(BaseModel):
    id: uuid.UUID
    pauta_id: uuid.UUID
    tipo: str
    corpo: dict
    status: str
    versao: int
    alerta_atualidade: str | None = None
    verificado_em: datetime | None = None
    criado_em: datetime

    model_config = {"from_attributes": True}


class ContentPieceUpdate(BaseModel):
    corpo: dict | None = None
    status: str | None = None


class ContentPieceManualCreate(BaseModel):
    pauta_id: uuid.UUID
    tipo: TIPOS_CONTENT_PIECE
    corpo: dict
    status: str = "rascunho"
