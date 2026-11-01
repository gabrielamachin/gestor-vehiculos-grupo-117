"""Conexión a PostgreSQL y sesión de SQLAlchemy.

El esquema de la base lo define database/schema.sql: la aplicación NO crea tablas
(no se usa Base.metadata.create_all). Los modelos solo mapean tablas existentes.
"""
from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

# create_engine no abre conexiones hasta la primera consulta.
engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Clase base de todos los modelos."""


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: una sesión por solicitud, cerrada al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Alias para usar en los routers: `def endpoint(db: DbSession): ...`
DbSession = Annotated[Session, Depends(get_db)]
