import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LecturaKilometraje(Base):
    """Mapea la tabla `lecturas_kilometraje` definida en database/schema.sql.

    `vehiculo_id` no declara ForeignKey a propósito: la FK vive en la base de datos y así este
    módulo no importa el modelo de Vehículos (cada módulo accede solo a sus propias tablas).
    """

    __tablename__ = "lecturas_kilometraje"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    vehiculo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    fecha: Mapped[date] = mapped_column(Date)
    kilometraje: Mapped[Decimal] = mapped_column(Numeric(10, 2))
