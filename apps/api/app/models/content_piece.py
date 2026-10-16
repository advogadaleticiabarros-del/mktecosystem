import copy
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Uuid, event, inspect
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ContentPiece(Base):
    __tablename__ = "content_pieces"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    pauta_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("pautas.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    corpo: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="rascunho")
    versao: Mapped[int] = mapped_column(Integer, default=1)
    alerta_atualidade: Mapped[str | None] = mapped_column(String(500), nullable=True)
    verificado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


# Material pronto nunca some (regra de 16/10/2026): quando o vídeo ou a imagem de uma peça muda, por qualquer caminho
# (API, script, publicador), a versão anterior fica em corpo["versoes_anteriores"] com a data da troca. A cópia da
# mídia é tirada ao carregar a peça, porque um script pode alterar o corpo no lugar (sem valor antigo no histórico).
CAMPOS_DE_MIDIA = ("video", "imagem", "imagens", "imagem_capa")


def _midia(corpo) -> dict:
    return {k: copy.deepcopy(corpo[k]) for k in CAMPOS_DE_MIDIA if k in (corpo or {})}


def _guardar_copia(peca: ContentPiece, *_args) -> None:
    peca.__dict__["_midia_salva"] = _midia(peca.__dict__.get("corpo"))


event.listen(ContentPiece, "load", _guardar_copia)
event.listen(ContentPiece, "refresh", _guardar_copia)


@event.listens_for(ContentPiece, "after_insert")
def _depois_de_criar(_mapper, _conn, peca: ContentPiece) -> None:
    _guardar_copia(peca)


@event.listens_for(ContentPiece, "before_update")
def _guardar_versao_anterior(_mapper, _conn, peca: ContentPiece) -> None:
    antes = peca.__dict__.get("_midia_salva")
    if antes is None:
        historico = inspect(peca).attrs.corpo.history
        antes = _midia(historico.deleted[0]) if historico.deleted else {}
    agora = _midia(peca.corpo)
    trocado = {k: v for k, v in antes.items() if agora.get(k) != v}
    if trocado:
        corpo = dict(peca.corpo or {})
        corpo["versoes_anteriores"] = [*(corpo.get("versoes_anteriores") or []),
                                       {**trocado, "em": datetime.now(timezone.utc).isoformat()}]
        peca.corpo = corpo
    peca.__dict__["_midia_salva"] = agora
