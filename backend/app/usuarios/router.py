"""Endpoints del módulo Usuarios (prefijo /usuarios)."""
from fastapi import APIRouter

from app.core.database import DbSession
from app.core.security import UsuarioIdActual
from app.usuarios import service
from app.usuarios.schemas import TokenRespuesta, UsuarioLogin, UsuarioRegistro, UsuarioRespuesta

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioRespuesta, status_code=201)
def registrar(datos: UsuarioRegistro, db: DbSession):
    return service.registrar(db, datos)


@router.post("/login", response_model=TokenRespuesta)
def login(datos: UsuarioLogin, db: DbSession):
    return TokenRespuesta(access_token=service.login(db, datos))


@router.get("/me", response_model=UsuarioRespuesta)
def perfil(db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener_perfil(db, usuario_id)
