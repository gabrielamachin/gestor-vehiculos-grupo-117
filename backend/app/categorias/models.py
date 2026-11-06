from sqlalchemy import Boolean, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Categoria(Base):
    """Mapea la tabla `categorias_gasto` definida en database/schema.sql.

    Es un catálogo: las filas se cargan con INSERT (ver los datos iniciales de schema.sql);
    la aplicación solo las lee.
    """

    __tablename__ = "categorias_gasto"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(30))
    nombre: Mapped[str] = mapped_column(String(60))
    tipo_costo: Mapped[str] = mapped_column(String(10))
    activa: Mapped[bool] = mapped_column(Boolean)
