"""Acceso a datos de la tabla `lecturas_kilometraje`. Sin reglas de negocio ni commits."""
import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.kilometraje.models import LecturaKilometraje as Lectura


def listar_por_vehiculo(db: Session, vehiculo_id: uuid.UUID) -> list[Lectura]:
    consulta = select(Lectura).where(Lectura.vehiculo_id == vehiculo_id).order_by(Lectura.fecha.desc())
    return list(db.scalars(consulta))


def obtener(db: Session, lectura_id: uuid.UUID) -> Lectura | None:
    return db.get(Lectura, lectura_id)


def obtener_por_fecha(db: Session, vehiculo_id: uuid.UUID, fecha: date) -> Lectura | None:
    return db.scalar(select(Lectura).where(Lectura.vehiculo_id == vehiculo_id, Lectura.fecha == fecha))


def ultima(db: Session, vehiculo_id: uuid.UUID) -> Lectura | None:
    consulta = select(Lectura).where(Lectura.vehiculo_id == vehiculo_id).order_by(Lectura.fecha.desc()).limit(1)
    return db.scalar(consulta)


def anterior_a(db: Session, vehiculo_id: uuid.UUID, fecha: date, excluir_id: uuid.UUID | None = None) -> Lectura | None:
    """Lectura más reciente con fecha estrictamente anterior (se excluye la que se está editando)."""
    consulta = select(Lectura).where(Lectura.vehiculo_id == vehiculo_id, Lectura.fecha < fecha)
    if excluir_id is not None:
        consulta = consulta.where(Lectura.id != excluir_id)
    return db.scalar(consulta.order_by(Lectura.fecha.desc()).limit(1))


def posterior_a(db: Session, vehiculo_id: uuid.UUID, fecha: date, excluir_id: uuid.UUID | None = None) -> Lectura | None:
    """Lectura más antigua con fecha estrictamente posterior (se excluye la que se está editando)."""
    consulta = select(Lectura).where(Lectura.vehiculo_id == vehiculo_id, Lectura.fecha > fecha)
    if excluir_id is not None:
        consulta = consulta.where(Lectura.id != excluir_id)
    return db.scalar(consulta.order_by(Lectura.fecha.asc()).limit(1))


def crear(db: Session, vehiculo_id: uuid.UUID, fecha: date, kilometraje: Decimal) -> Lectura:
    lectura = Lectura(vehiculo_id=vehiculo_id, fecha=fecha, kilometraje=kilometraje)
    db.add(lectura)
    db.flush()  # obtiene el id generado por la base
    return lectura


def actualizar(db: Session, lectura: Lectura, fecha: date, kilometraje: Decimal) -> Lectura:
    lectura.fecha = fecha
    lectura.kilometraje = kilometraje
    db.flush()
    return lectura


def eliminar(db: Session, lectura: Lectura) -> None:
    db.delete(lectura)
    db.flush()
