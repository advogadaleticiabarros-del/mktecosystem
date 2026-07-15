import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Pauta(Base):
    __tablename__ = "pautas"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    titulo: Mapped[str] = mapped_column(String(300))
    angulo: Mapped[str] = mapped_column(String(50))
    area: Mapped[str] = mapped_column(String(100))
    origem: Mapped[str] = mapped_column(String(20))
    fonte: Mapped[str] = mapped_column(String(200))
    relevante_para_conteudo: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="sugerida")
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
