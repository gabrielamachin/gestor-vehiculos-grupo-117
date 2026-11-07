"""Esquemas de salida del módulo Indicadores. Reflejan los resultados de resultados.py."""
import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.core.tipos import Numero


class _Salida(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CostoPorKmRespuesta(_Salida):
    estado: Literal["ok", "sin_lecturas", "sin_recorrido"]
    costo_por_km: Numero | None
    km_recorridos: Numero | None
    total_gastado: Numero


class ItemCategoriaRespuesta(_Salida):
    categoria_id: int
    codigo: str
    nombre: str
    tipo_costo: Literal["fijo", "variable"]
    total: Numero
    cantidad: int
    porcentaje: Numero


class GastoPorCategoriaRespuesta(_Salida):
    desde: date | None
    hasta: date | None
    total: Numero
    total_fijo: Numero
    total_variable: Numero
    categorias: list[ItemCategoriaRespuesta]


class AlertaCombustibleRespuesta(_Salida):
    estado: Literal["sin_datos", "historial_insuficiente", "normal", "alerta"]
    mes_evaluado: date | None
    gasto_mes: Numero | None
    promedio_historico: Numero | None
    desvio_pct: Numero | None
    meses_en_historial: int
    umbral_pct: Numero


class ProximoMantenimientoRespuesta(_Salida):
    plan_id: uuid.UUID
    nombre: str
    intervalo_km: Numero
    ultimo_km: Numero | None
    proximo_km: Numero
    km_restantes: Numero | None
    estado: Literal["sin_lecturas", "al_dia", "proximo", "vencido"]
    base: Literal["ultimo_mantenimiento", "multiplos"]


class SenalRespuesta(_Salida):
    codigo: str
    descripcion: str
    cumplida: bool


class OrientacionReparacionRespuesta(_Salida):
    estado: Literal["sin_datos", "reparar", "evaluar", "considerar_reemplazo"]
    mensaje: str
    senales: list[SenalRespuesta]
    aviso: str


class ResumenRespuesta(_Salida):
    costo_por_km: CostoPorKmRespuesta
    gasto_por_categoria: GastoPorCategoriaRespuesta
    alerta_combustible: AlertaCombustibleRespuesta
    proximos_mantenimientos: list[ProximoMantenimientoRespuesta]
    reparar_o_reemplazar: OrientacionReparacionRespuesta
