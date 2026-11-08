import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, SmallInteger, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Gasto(Base):
    """Mapea la tabla `gastos` definida en database/schema.sql.

    Las claves foráneas (vehículo, categoría y plan de mantenimiento) no se declaran como
    ForeignKey a propósito: viven en la base de datos y así este módulo no importa los modelos
    de otros módulos (cada módulo accede solo a sus propias tablas).
    """

    __tablename__ = "gastos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    vehiculo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    categoria_id: Mapped[int] = mapped_column(SmallInteger)
    plan_mantenimiento_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    fecha: Mapped[date] = mapped_column(Date)
    kilometraje: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
