"""Esquemas de entrada y salida del módulo Gastos (primera capa de validación)."""
import uuid
from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator, model_validator

from app.core.tipos import FechaNoFutura, Kilometros, Monto

# El detalle es opcional; la columna es TEXT, se limita para evitar abusos.
Descripcion = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]


class _CamposDeGasto(BaseModel):
    categoria_id: Annotated[int, Field(gt=0)]
    plan_mantenimiento_id: uuid.UUID | None = None
    monto: Monto
    fecha: FechaNoFutura
    kilometraje: Kilometros | None = None
    descripcion: Descripcion | None = None

    @field_validator("descripcion")
    @classmethod
    def _vacia_es_none(cls, valor: str | None) -> str | None:
        return valor or None

    @model_validator(mode="after")
    def _plan_requiere_kilometraje(self):
        # Mismo criterio que el CHECK chk_gastos_plan_requiere_km de la base.
        if self.plan_mantenimiento_id is not None and self.kilometraje is None:
            raise ValueError("El kilometraje es obligatorio al asociar el gasto a un plan de mantenimiento")
        return self


class GastoCrear(_CamposDeGasto):
    vehiculo_id: uuid.UUID


class GastoActualizar(_CamposDeGasto):
    """Reemplaza los datos del gasto; el gasto no cambia de vehículo."""


class GastoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    vehiculo_id: uuid.UUID
    categoria_id: int
    plan_mantenimiento_id: uuid.UUID | None
    monto: Monto
    fecha: date
    kilometraje: Kilometros | None
    descripcion: str | None
