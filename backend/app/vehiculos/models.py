import uuid
from decimal import Decimal

from sqlalchemy import Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Vehiculo(Base):
    """Mapea la tabla `vehiculos` definida en database/schema.sql.

    `usuario_id` no declara ForeignKey a propósito: la FK vive en la base de datos y así este
    módulo no importa el modelo de Usuarios (cada módulo accede solo a sus propias tablas).
    """

    __tablename__ = "vehiculos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    alias: Mapped[str] = mapped_column(String(100))
    kilometraje_inicial: Mapped[Decimal] = mapped_column(Numeric(10, 2))
