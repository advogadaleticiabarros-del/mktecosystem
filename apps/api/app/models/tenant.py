import uuid

from sqlalchemy import JSON, Boolean, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    nicho: Mapped[str] = mapped_column(String(100))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)


class TenantConfig(Base):
    __tablename__ = "tenant_configs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), unique=True)
    voz: Mapped[dict] = mapped_column(JSON, default=dict)
    identidade_visual: Mapped[dict] = mapped_column(JSON, default=dict)
    ctas: Mapped[dict] = mapped_column(JSON, default=dict)
    regras_compliance: Mapped[dict] = mapped_column(JSON, default=dict)
    canais: Mapped[dict] = mapped_column(JSON, default=dict)
