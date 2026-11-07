"""Endpoints del módulo Mantenimiento (prefijo /mantenimiento). Todos requieren autenticación."""
import uuid

from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.mantenimiento import service
from app.mantenimiento.schemas import PlanActualizar, PlanCrear, PlanRespuesta

router = APIRouter(prefix="/mantenimiento", tags=["Mantenimiento"])


@router.get("", response_model=list[PlanRespuesta])
def listar(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Planes de mantenimiento de un vehículo, ordenados por nombre."""
    return service.listar(db, usuario_id, vehiculo_id)


@router.post("", response_model=PlanRespuesta, status_code=201)
def crear(datos: PlanCrear, db: DbSession, usuario_id: UsuarioIdActual):
    return service.crear(db, usuario_id, datos)


@router.get("/{plan_id}", response_model=PlanRespuesta)
def obtener(plan_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener(db, plan_id, usuario_id)


@router.put("/{plan_id}", response_model=PlanRespuesta)
def actualizar(plan_id: uuid.UUID, datos: PlanActualizar, db: DbSession, usuario_id: UsuarioIdActual):
    return service.actualizar(db, plan_id, usuario_id, datos)


@router.delete("/{plan_id}", status_code=204)
def eliminar(plan_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    service.eliminar(db, plan_id, usuario_id)
