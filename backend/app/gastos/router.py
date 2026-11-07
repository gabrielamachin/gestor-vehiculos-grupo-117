"""Endpoints del módulo Gastos (prefijo /gastos). Todos requieren autenticación."""
import uuid
from datetime import date

from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.gastos import service
from app.gastos.schemas import GastoActualizar, GastoCrear, GastoRespuesta

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.get("", response_model=list[GastoRespuesta])
def listar(
    vehiculo_id: uuid.UUID,
    db: DbSession,
    usuario_id: UsuarioIdActual,
    desde: date | None = None,
    hasta: date | None = None,
    categoria_id: int | None = None,
):
    """Gastos de un vehículo, del más reciente al más antiguo. Filtros opcionales por fecha y categoría."""
    return service.listar(db, usuario_id, vehiculo_id, desde, hasta, categoria_id)


@router.post("", response_model=GastoRespuesta, status_code=201)
def crear(datos: GastoCrear, db: DbSession, usuario_id: UsuarioIdActual):
    return service.crear(db, usuario_id, datos)


@router.get("/{gasto_id}", response_model=GastoRespuesta)
def obtener(gasto_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener(db, gasto_id, usuario_id)


@router.put("/{gasto_id}", response_model=GastoRespuesta)
def actualizar(gasto_id: uuid.UUID, datos: GastoActualizar, db: DbSession, usuario_id: UsuarioIdActual):
    return service.actualizar(db, gasto_id, usuario_id, datos)


@router.delete("/{gasto_id}", status_code=204)
def eliminar(gasto_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    service.eliminar(db, gasto_id, usuario_id)
