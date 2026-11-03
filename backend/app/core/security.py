"""Hash de contraseñas y tokens JWT.

Infraestructura compartida: no depende de ningún módulo. Por eso `get_usuario_id_actual`
devuelve solo el id que viene en el token; cargar el usuario completo es tarea del módulo Usuarios.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.errors import NoAutenticado

# auto_error=False: si falta el token respondemos nosotros con 401 (FastAPI respondería 403).
_esquema_bearer = HTTPBearer(auto_error=False)


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
    credenciales: Annotated[HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)],
) -> uuid.UUID:
    """Dependencia de FastAPI: id del usuario autenticado. Responde 401 si no hay token válido."""
    if credenciales is None:
        raise NoAutenticado("Falta el token de autenticación")
    return decodificar_token(credenciales.credentials)


# Alias para usar en los routers: `def endpoint(usuario_id: UsuarioIdActual): ...`
UsuarioIdActual = Annotated[uuid.UUID, Depends(get_usuario_id_actual)]
