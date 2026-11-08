"""Hash de contraseñas y tokens JWT.

Infraestructura compartida: no depende de ningún módulo. Por eso `get_usuario_id_actual`
devuelve solo el id que viene en el token; cargar el usuario completo es tarea del módulo Usuarios.

El token puede llegar de dos maneras:
- Cookie `gestor_sesion` (HttpOnly): la usa el navegador. JavaScript no puede leerla. Ver POST/DELETE /usuarios/sesion.
- Header `Authorization: Bearer ...`: la usan Swagger, los tests y cualquier cliente que no sea el navegador.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.errors import NoAutenticado

# auto_error=False: si falta el token respondemos nosotros con 401 (FastAPI respondería 403).
_esquema_bearer = HTTPBearer(auto_error=False)

NOMBRE_COOKIE_SESION = "gestor_sesion"


def hashear_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:  # p. ej. contraseña de más de 72 bytes
        return False


def crear_token(usuario_id: uuid.UUID) -> str:
    settings = get_settings()
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "iat": ahora,
        "exp": ahora + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decodificar_token(token: str) -> uuid.UUID:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise NoAutenticado("Token inválido o vencido")


def get_usuario_id_actual(
    request: Request,
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)],
) -> uuid.UUID:
    """Dependencia de FastAPI: id del usuario autenticado. Responde 401 si no hay token válido.

    Si llega el header Authorization se usa ese (y si es inválido se rechaza, sin probar la cookie);
    si no, se usa la cookie de sesión.
    """
    if credenciales is not None:
        return decodificar_token(credenciales.credentials)
    token = request.cookies.get(NOMBRE_COOKIE_SESION)
    if token:
        return decodificar_token(token)
    raise NoAutenticado("Falta el token de autenticación")


def establecer_cookie_de_sesion(response: Response, token: str) -> None:
    """Guarda el JWT en una cookie HttpOnly. Dura lo mismo que el token.

    SameSite=Lax: el navegador no la envía en solicitudes POST/PUT/DELETE originadas en otros sitios. 
    Secure se activa con COOKIE_SECURE=true (producción, que usa HTTPS).
    """
    settings = get_settings()
    response.set_cookie(
        key=NOMBRE_COOKIE_SESION,
        value=token,
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
    )


def borrar_cookie_de_sesion(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(
        key=NOMBRE_COOKIE_SESION, path="/", httponly=True, secure=settings.cookie_secure, samesite="lax"
    )


# Alias para usar en los routers: `def endpoint(usuario_id: UsuarioIdActual): ...`
UsuarioIdActual = Annotated[uuid.UUID, Depends(get_usuario_id_actual)]
