import uuid
from decimal import Decimal

from sqlalchemy import Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PlanMantenimiento(Base):
    """Mapea la tabla `planes_mantenimiento` definida en database/schema.sql.

    `vehiculo_id` no declara ForeignKey a propósito: la FK vive en la base de datos y así este
    módulo no importa el modelo de Vehículos (cada módulo accede solo a sus propias tablas).
    """

    __tablename__ = "planes_mantenimiento"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    vehiculo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    nombre: Mapped[str] = mapped_column(String(100))
    intervalo_km: Mapped[Decimal] = mapped_column(Numeric(10, 2))
