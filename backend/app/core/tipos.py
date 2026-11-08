"""Tipos compartidos para esquemas Pydantic.

Pydantic v2 serializa `Decimal` como string en JSON ("12000.50"). Estos tipos validan con
Decimal (sin errores de redondeo) pero se entregan al frontend como número JSON.
"""
from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, Field, PlainSerializer

_A_NUMERO_JSON = PlainSerializer(float, return_type=float, when_used="json")

# Coincide con NUMERIC(10,2) de la base: kilometrajes no negativos, hasta 2 decimales.
Kilometros = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2), _A_NUMERO_JSON]

# Coincide con NUMERIC(12,2): montos estrictamente positivos, hasta 2 decimales.
Monto = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2), _A_NUMERO_JSON]

# Para valores calculados que se entregan como número JSON (sin restricciones de entrada).
Numero = Annotated[Decimal, _A_NUMERO_JSON]


def _validar_no_futura(valor: date) -> date:
    if valor > date.today():
        raise ValueError("La fecha no puede ser futura")
    return valor


# Para datos de ENTRADA (la base lo refuerza con CHECK (fecha <= CURRENT_DATE)).
FechaNoFutura = Annotated[date, AfterValidator(_validar_no_futura)]
