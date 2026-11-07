"""Esquemas de entrada y salida del módulo Mantenimiento (primera capa de validación)."""
import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.core.tipos import Kilometros

# 100 = largo de la columna `nombre`.
Nombre = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
# Cada cuántos km se repite: estrictamente positivo (la base lo refuerza con CHECK intervalo_km > 0).
IntervaloKm = Annotated[Kilometros, Field(gt=0)]


class PlanCrear(BaseModel):
    vehiculo_id: uuid.UUID
    nombre: Nombre
    intervalo_km: IntervaloKm


class PlanActualizar(BaseModel):
    """Se puede corregir nombre e intervalo; el plan no cambia de vehículo."""

    nombre: Nombre
    intervalo_km: IntervaloKm


class PlanRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vehiculo_id: uuid.UUID
    nombre: str
    intervalo_km: Kilometros
