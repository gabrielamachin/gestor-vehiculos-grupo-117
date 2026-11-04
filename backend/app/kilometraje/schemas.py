"""Esquemas de entrada y salida del módulo Kilometraje (primera capa de validación)."""
import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

from app.core.tipos import FechaNoFutura, Kilometros


class LecturaCrear(BaseModel):
    vehiculo_id: uuid.UUID
    fecha: FechaNoFutura
    kilometraje: Kilometros


class LecturaActualizar(BaseModel):
    """Se puede corregir fecha y kilometraje; la lectura no cambia de vehículo."""

    fecha: FechaNoFutura
    kilometraje: Kilometros


class LecturaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vehiculo_id: uuid.UUID
    fecha: date
    kilometraje: Kilometros
