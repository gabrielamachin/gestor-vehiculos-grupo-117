"""Lógica de negocio del módulo Mantenimiento. No conoce HTTP: lanza errores de dominio.

Interfaz para otros módulos:
- `obtener_plan_del_vehiculo`: la usa Gastos al asociar un gasto a un plan.
- `listar_planes_de_vehiculo`: la usa Indicadores para estimar el próximo mantenimiento.

Mantenimiento NO conoce los gastos (así se evita la dependencia circular con Gastos): el
cálculo del próximo mantenimiento, que necesita ambos, vive en Indicadores.
"""
import uuid
from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import Conflicto, NoEncontrado, ReglaDeNegocio
from app.mantenimiento import repository
from app.mantenimiento.models import PlanMantenimiento as Plan
from app.mantenimiento.schemas import PlanActualizar, PlanCrear
from app.vehiculos import service as vehiculos_service
from app.vehiculos.models import Vehiculo

_MENSAJE_NOMBRE = "Ya existe un plan con ese nombre para este vehículo"


def _es_nombre_duplicado(error: IntegrityError) -> bool:
    """Distingue el UNIQUE (vehiculo_id, nombre) de otras violaciones de integridad (p. ej. una FK)."""
    diag = getattr(error.orig, "diag", None)
    return getattr(diag, "constraint_name", None) == "uq_planes_vehiculo_nombre"


def _obtener_plan_de_usuario(db: Session, plan_id: uuid.UUID, usuario_id: uuid.UUID) -> tuple[Plan, Vehiculo]:
    """Un plan pertenece al usuario si su vehículo le pertenece (se verifica vía el módulo Vehículos)."""
    plan = repository.obtener(db, plan_id)
    if plan is None:
        raise NoEncontrado("Plan de mantenimiento no encontrado")
    try:
        vehiculo = vehiculos_service.obtener_de_usuario(db, plan.vehiculo_id, usuario_id)
    except NoEncontrado:
        # Mismo mensaje que si no existiera: no se revela que el plan es de otro usuario.
        raise NoEncontrado("Plan de mantenimiento no encontrado") from None
    return plan, vehiculo


def listar(db: Session, usuario_id: uuid.UUID, vehiculo_id: uuid.UUID) -> list[Plan]:
    vehiculos_service.obtener_de_usuario(db, vehiculo_id, usuario_id)
    return repository.listar_por_vehiculo(db, vehiculo_id)


def obtener(db: Session, plan_id: uuid.UUID, usuario_id: uuid.UUID) -> Plan:
    return _obtener_plan_de_usuario(db, plan_id, usuario_id)[0]


def crear(db: Session, usuario_id: uuid.UUID, datos: PlanCrear) -> Plan:
    vehiculo = vehiculos_service.obtener_de_usuario(db, datos.vehiculo_id, usuario_id)

    if repository.obtener_por_nombre(db, vehiculo.id, datos.nombre) is not None:
        raise Conflicto(_MENSAJE_NOMBRE)

    try:
        plan = repository.crear(db, vehiculo.id, datos.nombre, datos.intervalo_km)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_nombre_duplicado(error):  # dos solicitudes simultáneas con el mismo nombre
            raise Conflicto(_MENSAJE_NOMBRE) from error
        raise
    return plan


def actualizar(db: Session, plan_id: uuid.UUID, usuario_id: uuid.UUID, datos: PlanActualizar) -> Plan:
    plan, vehiculo = _obtener_plan_de_usuario(db, plan_id, usuario_id)

    existente = repository.obtener_por_nombre(db, vehiculo.id, datos.nombre)
    if existente is not None and existente.id != plan.id:
        raise Conflicto(_MENSAJE_NOMBRE)

    try:
        repository.actualizar(db, plan, datos.nombre, datos.intervalo_km)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_nombre_duplicado(error):
            raise Conflicto(_MENSAJE_NOMBRE) from error
        raise
    return plan


def eliminar(db: Session, plan_id: uuid.UUID, usuario_id: uuid.UUID) -> None:
    """Borra el plan. Los gastos asociados se conservan: solo pierden la asociación (ON DELETE SET NULL)."""
    plan, _ = _obtener_plan_de_usuario(db, plan_id, usuario_id)
    repository.eliminar(db, plan)
    db.commit()


# ---------- Interfaz para otros módulos (no verifican pertenencia del vehículo) ----------

def obtener_plan_del_vehiculo(db: Session, plan_id: uuid.UUID, vehiculo_id: uuid.UUID) -> Plan:
    """Para Gastos: el plan debe existir y ser de ese vehículo.

    Quien la llama ya verificó que el vehículo es del usuario. Mismo mensaje si el plan no existe
    o es de otro vehículo (la base también lo impide con la FK compuesta de `gastos`).
    """
    plan = repository.obtener(db, plan_id)
    if plan is None or plan.vehiculo_id != vehiculo_id:
        raise ReglaDeNegocio("El plan de mantenimiento no existe o no pertenece al vehículo")
    return plan


def listar_planes_de_vehiculo(db: Session, vehiculo_id: uuid.UUID) -> list[Plan]:
    """Para Indicadores: planes de un vehículo ya verificado."""
    return repository.listar_por_vehiculo(db, vehiculo_id)
