"""Lógica de negocio del módulo Usuarios. No conoce HTTP: lanza errores de dominio."""
import uuid
from functools import cache

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import Conflicto, NoAutenticado, NoEncontrado
from app.core.security import crear_token, hashear_password, verificar_password
from app.usuarios import repository
from app.usuarios.models import Usuario
from app.usuarios.schemas import UsuarioLogin, UsuarioRegistro


@cache
def _hash_de_relleno() -> str:
    return hashear_password("relleno-para-igualar-tiempos")


def registrar(db: Session, datos: UsuarioRegistro) -> Usuario:
    if repository.obtener_por_email(db, datos.email) is not None:
        raise Conflicto("Ya existe un usuario con ese email")

    try:
        usuario = repository.crear(db, datos.nombre, datos.email, hashear_password(datos.password))
        db.commit()
    except IntegrityError:
        # Dos registros simultáneos con el mismo email: la restricción UNIQUE de la base lo detiene.
        db.rollback()
        raise Conflicto("Ya existe un usuario con ese email")
    return usuario


def login(db: Session, datos: UsuarioLogin) -> str:
    """Devuelve un token JWT. El mismo mensaje para email inexistente y contraseña incorrecta."""
    usuario = repository.obtener_por_email(db, datos.email)
    if usuario is None:
        # Se verifica igual contra un hash de relleno para que el tiempo de respuesta no delate si el email existe.
        verificar_password(datos.password, _hash_de_relleno())
        raise NoAutenticado("Credenciales inválidas")
    if not verificar_password(datos.password, usuario.password_hash):
        raise NoAutenticado("Credenciales inválidas")
    return crear_token(usuario.id)


def obtener_perfil(db: Session, usuario_id: uuid.UUID) -> Usuario:
    usuario = repository.obtener_por_id(db, usuario_id)
    if usuario is None:  # token válido de un usuario que ya no existe
        raise NoEncontrado("Usuario no encontrado")
    return usuario
