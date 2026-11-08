"""Tipos de resultado de las consultas agregadas de Gastos.

Forman parte de la interfaz pública del módulo: Indicadores los importa desde acá
(nunca desde el repositorio ni del modelo).
"""
from datetime import date
from decimal import Decimal
from typing import NamedTuple


class TotalCategoria(NamedTuple):
    categoria_id: int
    total: Decimal
    cantidad: int


class TotalMes(NamedTuple):
    mes: date  # primer día del mes
    total: Decimal
