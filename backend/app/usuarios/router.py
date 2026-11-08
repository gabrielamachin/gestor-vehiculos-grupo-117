"""Endpoints del módulo Usuarios (prefijo /usuarios)."""
from fastapi import APIRouter, Response

from app.core.database import DbSession
from app.core.security import UsuarioIdActual, borrar_cookie_de_sesion, establecer_cookie_de_sesion
from app.usuarios import service
from app.usuarios.schemas import TokenRespuesta, UsuarioLogin, UsuarioRegistro, UsuarioRespuesta

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/registro", response_model=UsuarioRespuesta, status_code=201)
def registrar(datos: UsuarioRegistro, db: DbSession):
    return service.registrar(db, datos)


@router.post("/login", response_model=TokenRespuesta)
def login(datos: UsuarioLogin, db: DbSession):
    """Devuelve el token en el cuerpo. Para Swagger, scripts y clientes que no son el navegador."""
    return TokenRespuesta(access_token=service.login(db, datos))


@router.post("/sesion", response_model=UsuarioRespuesta)
def iniciar_sesion(datos: UsuarioLogin, db: DbSession, response: Response):
    """Inicia sesión para el navegador: el token va en una cookie HttpOnly y nunca llega al JavaScript."""
    usuario, token = service.iniciar_sesion(db, datos)
    establecer_cookie_de_sesion(response, token)
    return usuario


@router.delete("/sesion", status_code=204)
def cerrar_sesion(response: Response):
    """Cierra la sesión borrando la cookie. Es idempotente: no falla si no había sesión."""
    borrar_cookie_de_sesion(response)


@router.get("/me", response_model=UsuarioRespuesta)
def perfil(db: DbSession, usuario_id: UsuarioIdActual):
    return service.obtener_perfil(db, usuario_id)
