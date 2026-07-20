import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SocialConnection(Base):
    __tablename__ = "social_connections"
    __table_args__ = (
        UniqueConstraint("tenant_id", "plataforma", name="uq_social_connections_tenant_plataforma"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    plataforma: Mapped[str] = mapped_column(String(20))
    page_id: Mapped[str] = mapped_column(String(50))
    ig_user_id: Mapped[str] = mapped_column(String(50))
    nome_conta: Mapped[str] = mapped_column(String(200))
    access_token_encrypted: Mapped[str] = mapped_column(Text)
    expira_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ativo")
    conectado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
