"""Lógica de negocio del módulo Vehículos. No conoce HTTP: lanza errores de dominio.

`obtener_de_usuario` es la interfaz que usan los demás módulos (Gastos, Kilometraje,
Mantenimiento, Indicadores) para verificar la pertenencia antes de operar sobre un vehículo.
"""
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import Conflicto, NoEncontrado
from app.vehiculos import repository
from app.vehiculos.models import Vehiculo
from app.vehiculos.schemas import VehiculoActualizar, VehiculoCrear

_MENSAJE_ALIAS = "Ya tenés un vehículo con ese alias"


def _es_alias_duplicado(error: IntegrityError) -> bool:
    """Distingue el UNIQUE (usuario_id, alias) de otras violaciones de integridad (p. ej. una FK)."""
    diag = getattr(error.orig, "diag", None)
    return getattr(diag, "constraint_name", None) == "uq_vehiculos_usuario_alias"


def listar(db: Session, usuario_id: uuid.UUID) -> list[Vehiculo]:
    return repository.listar_por_usuario(db, usuario_id)


def obtener_de_usuario(db: Session, vehiculo_id: uuid.UUID, usuario_id: uuid.UUID) -> Vehiculo:
    """Devuelve el vehículo si pertenece al usuario; si no, 404 (sin revelar si existe)."""
    vehiculo = repository.obtener_de_usuario(db, vehiculo_id, usuario_id)
    if vehiculo is None:
        raise NoEncontrado("Vehículo no encontrado")
    return vehiculo


def crear(db: Session, usuario_id: uuid.UUID, datos: VehiculoCrear) -> Vehiculo:
    if repository.obtener_por_alias(db, usuario_id, datos.alias) is not None:
        raise Conflicto(_MENSAJE_ALIAS)

    try:
        vehiculo = repository.crear(db, usuario_id, datos.alias, datos.kilometraje_inicial)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_alias_duplicado(error):  # dos solicitudes simultáneas con el mismo alias
            raise Conflicto(_MENSAJE_ALIAS) from error
        raise
    return vehiculo


def actualizar(db: Session, vehiculo_id: uuid.UUID, usuario_id: uuid.UUID, datos: VehiculoActualizar) -> Vehiculo:
    vehiculo = obtener_de_usuario(db, vehiculo_id, usuario_id)

    existente = repository.obtener_por_alias(db, usuario_id, datos.alias)
    if existente is not None and existente.id != vehiculo.id:
        raise Conflicto(_MENSAJE_ALIAS)

    try:
        repository.actualizar_alias(db, vehiculo, datos.alias)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        if _es_alias_duplicado(error):
            raise Conflicto(_MENSAJE_ALIAS) from error
        raise
    return vehiculo


def eliminar(db: Session, vehiculo_id: uuid.UUID, usuario_id: uuid.UUID) -> None:
    """Borra el vehículo y, por ON DELETE CASCADE, sus gastos, lecturas y planes de mantenimiento."""
    vehiculo = obtener_de_usuario(db, vehiculo_id, usuario_id)
    repository.eliminar(db, vehiculo)
    db.commit()
