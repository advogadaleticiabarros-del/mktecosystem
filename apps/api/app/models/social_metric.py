import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SocialMetric(Base):
    __tablename__ = "social_metrics"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    tipo: Mapped[str] = mapped_column(String(20))
    referencia_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    metricas: Mapped[dict] = mapped_column(JSON, default=dict)
    coletado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
