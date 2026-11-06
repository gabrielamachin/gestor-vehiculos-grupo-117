"""Acceso a datos de la tabla `planes_mantenimiento`. Sin reglas de negocio ni commits."""
import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.mantenimiento.models import PlanMantenimiento as Plan


def listar_por_vehiculo(db: Session, vehiculo_id: uuid.UUID) -> list[Plan]:
    return list(db.scalars(select(Plan).where(Plan.vehiculo_id == vehiculo_id).order_by(Plan.nombre)))


def obtener(db: Session, plan_id: uuid.UUID) -> Plan | None:
    return db.get(Plan, plan_id)


def obtener_por_nombre(db: Session, vehiculo_id: uuid.UUID, nombre: str) -> Plan | None:
    return db.scalar(select(Plan).where(Plan.vehiculo_id == vehiculo_id, Plan.nombre == nombre))


def crear(db: Session, vehiculo_id: uuid.UUID, nombre: str, intervalo_km: Decimal) -> Plan:
    plan = Plan(vehiculo_id=vehiculo_id, nombre=nombre, intervalo_km=intervalo_km)
    db.add(plan)
    db.flush()  # obtiene el id generado por la base
    return plan


def actualizar(db: Session, plan: Plan, nombre: str, intervalo_km: Decimal) -> Plan:
    plan.nombre = nombre
    plan.intervalo_km = intervalo_km
    db.flush()
    return plan


def eliminar(db: Session, plan: Plan) -> None:
    db.delete(plan)
    db.flush()
