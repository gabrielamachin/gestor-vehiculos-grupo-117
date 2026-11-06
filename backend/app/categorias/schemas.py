from typing import Literal

from pydantic import BaseModel, ConfigDict


class CategoriaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    tipo_costo: Literal["fijo", "variable"]
    activa: bool
