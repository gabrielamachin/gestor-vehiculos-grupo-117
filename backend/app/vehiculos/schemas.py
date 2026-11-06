"""Esquemas de entrada y salida del módulo Vehículos (primera capa de validación)."""
import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from app.core.tipos import Kilometros

# 100 = largo de la columna `alias`.
Alias = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class VehiculoCrear(BaseModel):
    alias: Alias
    kilometraje_inicial: Kilometros


class VehiculoActualizar(BaseModel):
    """Solo se edita el alias. El kilometraje inicial es la base del costo por km y no se modifica."""

    alias: Alias


class VehiculoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    alias: str
    kilometraje_inicial: Kilometros
