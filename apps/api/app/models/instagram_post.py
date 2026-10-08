import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class InstagramPost(Base):
    """Cada publicação do perfil com suas métricas mais recentes (atualizadas todo dia)."""

    __tablename__ = "instagram_posts"
    __table_args__ = (UniqueConstraint("tenant_id", "media_id", name="uq_instagram_posts_tenant_media"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), index=True)
    media_id: Mapped[str] = mapped_column(String(40))
    publicado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    formato: Mapped[str] = mapped_column(String(20))  # Reels | Carrossel | Imagem
    area: Mapped[str] = mapped_column(String(30))
    legenda: Mapped[str | None] = mapped_column(Text, nullable=True)
    permalink: Mapped[str | None] = mapped_column(String(255), nullable=True)
    alcance: Mapped[int] = mapped_column(Integer, default=0)
    visualizacoes: Mapped[int] = mapped_column(Integer, default=0)
    curtidas: Mapped[int] = mapped_column(Integer, default=0)
    comentarios: Mapped[int] = mapped_column(Integer, default=0)
    compartilhamentos: Mapped[int] = mapped_column(Integer, default=0)
    salvamentos: Mapped[int] = mapped_column(Integer, default=0)
    interacoes: Mapped[int] = mapped_column(Integer, default=0)
    seguidores_ganhos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    visitas_perfil: Mapped[int | None] = mapped_column(Integer, nullable=True)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
