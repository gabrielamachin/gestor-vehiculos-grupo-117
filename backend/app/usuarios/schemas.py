"""Esquemas de entrada y salida. Primera capa de validación de la API (ver esquema-db.md, sección 6)."""
import uuid
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator

def _normalizar_email(valor: str) -> str:
    # El UNIQUE de la base distingue mayúsculas: se pasa a minúsculas para que
    # "A@x.com" y "a@x.com" sean el mismo usuario. 255 = largo de la columna.
    valor = valor.lower()
    if len(valor) > 255:
        raise ValueError("El email no puede superar los 255 caracteres")
    return valor


Email = Annotated[EmailStr, AfterValidator(_normalizar_email)]
Nombre = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]


class UsuarioRegistro(BaseModel):
    nombre: Nombre
    email: Email
    password: Annotated[str, Field(min_length=8)]

    @field_validator("password")
    @classmethod
    def _password_cabe_en_bcrypt(cls, valor: str) -> str:
        # bcrypt solo admite 72 bytes (un carácter con tilde ocupa 2).
        if len(valor.encode("utf-8")) > 72:
            raise ValueError("La contraseña no puede superar los 72 bytes")
        return valor


class UsuarioLogin(BaseModel):
    email: Email
    # No se repiten las reglas de longitud: no hay que revelar cómo son las contraseñas válidas.
    password: Annotated[str, Field(min_length=1, max_length=128)]


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nombre: str
    email: str


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"
