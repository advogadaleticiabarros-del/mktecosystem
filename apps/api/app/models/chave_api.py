import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ChaveApi(Base):
    """Chave de API de um serviço externo (ex.: OpenAI), guardada criptografada."""

    __tablename__ = "chaves_api"
    __table_args__ = (UniqueConstraint("tenant_id", "provedor", name="uq_chaves_api_tenant_provedor"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    provedor: Mapped[str] = mapped_column(String(30))
    chave_criptografada: Mapped[str] = mapped_column(Text)
    final: Mapped[str] = mapped_column(String(8))
    validada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
