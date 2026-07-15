import uuid

from sqlalchemy import JSON, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class MarketingMemory(Base):
    __tablename__ = "marketing_memory"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    content_piece_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("content_pieces.id"))
    tema: Mapped[str] = mapped_column(String(300))
    angulo: Mapped[str] = mapped_column(String(50))
    formato: Mapped[str] = mapped_column(String(20))
    metricas: Mapped[dict] = mapped_column(JSON, default=dict)
    aprendizado: Mapped[str | None] = mapped_column(String(2000), nullable=True)
