import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


def _agora() -> datetime:
    return datetime.now(timezone.utc)


class RecomendacaoStatus(Base):
    """O que a usuária decidiu sobre uma melhoria do diagnóstico ("feita" ou "ignorada")."""

    __tablename__ = "recomendacoes_status"
    __table_args__ = (UniqueConstraint("tenant_id", "chave", name="uq_recomendacoes_status_tenant_chave"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    chave: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(20))
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_agora)


class GooglePost(Base):
    """Post do Perfil da Empresa criado no Orbit. Vai para o Google quando `status="aprovado"`
    e `publicar_em` chega (job de hora em hora)."""

    __tablename__ = "google_posts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    texto: Mapped[str] = mapped_column(Text)
    botao: Mapped[str | None] = mapped_column(String(20), nullable=True)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    imagem_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    publicar_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_agora)
    status: Mapped[str] = mapped_column(String(20), default="rascunho")
    google_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    link_publicado: Mapped[str | None] = mapped_column(String(500), nullable=True)
    erro: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_agora)
