"""Endpoints del módulo Kilometraje (prefijo /kilometraje). Todos requieren autenticación."""
import uuid

from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.kilometraje import service
from app.kilometraje.schemas import LecturaActualizar, LecturaCrear, LecturaRespuesta

router = APIRouter(prefix="/kilometraje", tags=["Kilometraje"])


@router.get("", response_model=list[LecturaRespuesta])
def listar(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Lecturas de un vehículo, de la más reciente a la más antigua."""
    return service.listar(db, usuario_id, vehiculo_id)


# Debe ir antes de "/{lectura_id}" para que "ultima" no se interprete como un id.
@router.get("/ultima", response_model=LecturaRespuesta | None)
def ultima(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    """Kilometraje actual del vehículo (su última lectura). Responde null si todavía no tiene lecturas."""
    return service.ultima(db, usuario_id, vehiculo_id)


@router.post("", response_model=LecturaRespuesta, status_code=201)
def crear(datos: LecturaCrear, db: DbSession, usuario_id: UsuarioIdActual):
    return service.crear(db, usuario_id, datos)


@router.get("/{lectura_id}", response_model=LecturaRespuesta)
def obtener(lectura_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener(db, lectura_id, usuario_id)


@router.put("/{lectura_id}", response_model=LecturaRespuesta)
def actualizar(lectura_id: uuid.UUID, datos: LecturaActualizar, db: DbSession, usuario_id: UsuarioIdActual):
    return service.actualizar(db, lectura_id, usuario_id, datos)


@router.delete("/{lectura_id}", status_code=204)
def eliminar(lectura_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    service.eliminar(db, lectura_id, usuario_id)
