"""Acceso a datos de la tabla `usuarios`. Sin reglas de negocio ni commits (los hace el servicio)."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.usuarios.models import Usuario


def obtener_por_id(db: Session, usuario_id: uuid.UUID) -> Usuario | None:
    return db.get(Usuario, usuario_id)


def obtener_por_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email))


def crear(db: Session, nombre: str, email: str, password_hash: str) -> Usuario:
    usuario = Usuario(nombre=nombre, email=email, password_hash=password_hash)
    db.add(usuario)
    db.flush()  # obtiene el id generado por la base
    return usuario
