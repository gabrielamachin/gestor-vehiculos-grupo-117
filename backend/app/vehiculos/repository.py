"""Acceso a datos de la tabla `vehiculos`. Sin reglas de negocio ni commits (los hace el servicio)."""
import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.vehiculos.models import Vehiculo


def listar_por_usuario(db: Session, usuario_id: uuid.UUID) -> list[Vehiculo]:
    consulta = select(Vehiculo).where(Vehiculo.usuario_id == usuario_id).order_by(Vehiculo.alias)
    return list(db.scalars(consulta))


def obtener_de_usuario(db: Session, vehiculo_id: uuid.UUID, usuario_id: uuid.UUID) -> Vehiculo | None:
    """Filtra por id Y por propietario: un vehículo ajeno es indistinguible de uno inexistente."""
    consulta = select(Vehiculo).where(Vehiculo.id == vehiculo_id, Vehiculo.usuario_id == usuario_id)
    return db.scalar(consulta)


def obtener_por_alias(db: Session, usuario_id: uuid.UUID, alias: str) -> Vehiculo | None:
    consulta = select(Vehiculo).where(Vehiculo.usuario_id == usuario_id, Vehiculo.alias == alias)
    return db.scalar(consulta)


def crear(db: Session, usuario_id: uuid.UUID, alias: str, kilometraje_inicial: Decimal) -> Vehiculo:
    vehiculo = Vehiculo(usuario_id=usuario_id, alias=alias, kilometraje_inicial=kilometraje_inicial)
    db.add(vehiculo)
    db.flush()  # obtiene el id generado por la base
    return vehiculo


def actualizar_alias(db: Session, vehiculo: Vehiculo, alias: str) -> Vehiculo:
    vehiculo.alias = alias
    db.flush()
    return vehiculo


def eliminar(db: Session, vehiculo: Vehiculo) -> None:
    db.delete(vehiculo)
    db.flush()
