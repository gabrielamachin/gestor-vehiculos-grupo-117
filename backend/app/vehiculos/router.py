"""Endpoints del módulo Vehículos (prefijo /vehiculos). Todos requieren autenticación."""
import uuid

from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.vehiculos import service
from app.vehiculos.schemas import VehiculoActualizar, VehiculoCrear, VehiculoRespuesta

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.get("", response_model=list[VehiculoRespuesta])
def listar(db: DbSession, usuario_id: UsuarioIdActual):
    return service.listar(db, usuario_id)


@router.post("", response_model=VehiculoRespuesta, status_code=201)
def crear(datos: VehiculoCrear, db: DbSession, usuario_id: UsuarioIdActual):
    return service.crear(db, usuario_id, datos)


@router.get("/{vehiculo_id}", response_model=VehiculoRespuesta)
def obtener(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener_de_usuario(db, vehiculo_id, usuario_id)


@router.put("/{vehiculo_id}", response_model=VehiculoRespuesta)
def actualizar(vehiculo_id: uuid.UUID, datos: VehiculoActualizar, db: DbSession, usuario_id: UsuarioIdActual):
    return service.actualizar(db, vehiculo_id, usuario_id, datos)


@router.delete("/{vehiculo_id}", status_code=204)
def eliminar(vehiculo_id: uuid.UUID, db: DbSession, usuario_id: UsuarioIdActual):
    service.eliminar(db, vehiculo_id, usuario_id)
