import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ScheduledPost(Base):
    __tablename__ = "scheduled_posts"
    __table_args__ = (
        UniqueConstraint("content_piece_id", name="uq_scheduled_posts_content_piece"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"))
    content_piece_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("content_pieces.id"), nullable=True
    )
    titulo: Mapped[str] = mapped_column(String(300))
    canal: Mapped[str] = mapped_column(String(20))
    formato: Mapped[str] = mapped_column(String(20))
    data_agendada: Mapped[date] = mapped_column(Date)
    horario: Mapped[str] = mapped_column(String(5), default="11:00")
    status: Mapped[str] = mapped_column(String(20), default="planejado")
    platform_post_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tentativas: Mapped[int] = mapped_column(Integer, default=0)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
