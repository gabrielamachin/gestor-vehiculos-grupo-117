"""Tipos de resultado de los indicadores (datos puros, sin dependencias de FastAPI ni de la base)."""
import uuid
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class CostoPorKm:
    estado: str  # ok | sin_lecturas | sin_recorrido
    costo_por_km: Decimal | None
    km_recorridos: Decimal | None
    total_gastado: Decimal


@dataclass(frozen=True)
class ItemCategoria:
    categoria_id: int
    codigo: str
    nombre: str
    tipo_costo: str
    total: Decimal
    cantidad: int
    porcentaje: Decimal


@dataclass(frozen=True)
class GastoPorCategoria:
    desde: date | None
    hasta: date | None
    total: Decimal
    total_fijo: Decimal
    total_variable: Decimal
    categorias: tuple[ItemCategoria, ...]


@dataclass(frozen=True)
class AlertaCombustible:
    estado: str  # sin_datos | historial_insuficiente | normal | alerta
    mes_evaluado: date | None
    gasto_mes: Decimal | None
    promedio_historico: Decimal | None
    desvio_pct: Decimal | None
    meses_en_historial: int
    umbral_pct: Decimal


@dataclass(frozen=True)
class EstimacionMantenimiento:
    proximo_km: Decimal
    km_restantes: Decimal | None
    estado: str  # sin_lecturas | al_dia | proximo | vencido
    base: str  # ultimo_mantenimiento | multiplos


@dataclass(frozen=True)
class ProximoMantenimiento:
    plan_id: uuid.UUID
    nombre: str
    intervalo_km: Decimal
    ultimo_km: Decimal | None
    proximo_km: Decimal
    km_restantes: Decimal | None
    estado: str
    base: str


@dataclass(frozen=True)
class Senal:
    codigo: str
    descripcion: str
    cumplida: bool


@dataclass(frozen=True)
class OrientacionReparacion:
    estado: str  # sin_datos | reparar | evaluar | considerar_reemplazo
    mensaje: str
    senales: tuple[Senal, ...]
    aviso: str


@dataclass(frozen=True)
class ResumenIndicadores:
    costo_por_km: CostoPorKm
    gasto_por_categoria: GastoPorCategoria
    alerta_combustible: AlertaCombustible
    proximos_mantenimientos: tuple[ProximoMantenimiento, ...]
    reparar_o_reemplazar: OrientacionReparacion
