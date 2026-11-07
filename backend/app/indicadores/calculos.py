"""Fórmulas de los indicadores como funciones puras.

No acceden a la base ni a otros módulos: reciben números y devuelven resultados, por lo que se
prueban con pruebas unitarias simples. Los umbrales son constantes del módulo y son PROVISORIOS:
están pensados para ajustarse con datos reales.
"""
from datetime import date
from decimal import ROUND_CEILING, ROUND_HALF_UP, Decimal
from typing import Iterable

from app.indicadores.resultados import (
    AlertaCombustible,
    CostoPorKm,
    EstimacionMantenimiento,
    OrientacionReparacion,
    Senal,
)

# ---- Umbrales ----
UMBRAL_COMBUSTIBLE = Decimal("0.20")        # el mes evaluado supera al promedio en 20% o más -> alerta
MIN_MESES_HISTORIAL = 3                     # meses previos con gasto necesarios para comparar
UMBRAL_PROXIMO = Decimal("0.10")            # a menos del 10% del intervalo del vencimiento -> "próximo"
UMBRAL_PESO_REPARACIONES = Decimal("0.35")  # reparaciones >= 35% del gasto de los últimos 12 meses
FACTOR_AUMENTO_REPARACIONES = Decimal("1.5")  # últimos 6 meses >= 1,5 veces los 6 meses previos
KM_ELEVADO = Decimal("150000")

AVISO_ORIENTACION = (
    "Orientación basada solo en los gastos que cargaste. No es una tasación ni reemplaza la opinión de un mecánico."
)

_CENTAVOS = Decimal("0.01")


def _dos_decimales(valor: Decimal) -> Decimal:
    return valor.quantize(_CENTAVOS, rounding=ROUND_HALF_UP)


def porcentaje(parte: Decimal, total: Decimal) -> Decimal:
    """`parte` como porcentaje de `total`, con 2 decimales (0 si el total es 0)."""
    if total <= 0:
        return Decimal("0.00")
    return _dos_decimales(parte * 100 / total)


def costo_por_km(total_gastado: Decimal, km_inicial: Decimal, km_actual: Decimal | None) -> CostoPorKm:
    """Costo real por km = total gastado / km recorridos desde el kilometraje inicial."""
    if km_actual is None:
        return CostoPorKm("sin_lecturas", None, None, total_gastado)
    recorridos = km_actual - km_inicial
    if recorridos <= 0:
        return CostoPorKm("sin_recorrido", None, Decimal("0"), total_gastado)
    return CostoPorKm("ok", _dos_decimales(total_gastado / recorridos), recorridos, total_gastado)


def evaluar_combustible(
    serie_mensual: Iterable[tuple[date, Decimal]],
    umbral: Decimal = UMBRAL_COMBUSTIBLE,
    min_meses_historial: int = MIN_MESES_HISTORIAL,
) -> AlertaCombustible:
    """Compara el mes más reciente con gasto contra el promedio de los meses anteriores con gasto.

    Se promedian solo los meses con gasto registrado (un mes sin cargas no baja el promedio).
    Alerta si el mes evaluado es >= promedio * (1 + umbral).
    """
    umbral_pct = umbral * 100
    meses = sorted(serie_mensual, key=lambda fila: fila[0])
    if not meses:
        return AlertaCombustible("sin_datos", None, None, None, None, 0, umbral_pct)

    *historial, (mes, gasto) = meses
    cantidad = len(historial)
    if cantidad < min_meses_historial:
        return AlertaCombustible("historial_insuficiente", mes, gasto, None, None, cantidad, umbral_pct)

    promedio = sum((total for _, total in historial), Decimal("0")) / cantidad
    desvio = _dos_decimales((gasto - promedio) / promedio * 100)
    estado = "alerta" if gasto >= promedio * (1 + umbral) else "normal"
    return AlertaCombustible(estado, mes, gasto, _dos_decimales(promedio), desvio, cantidad, umbral_pct)


def estimar_proximo_mantenimiento(
    intervalo_km: Decimal,
    ultimo_km: Decimal | None,
    km_actual: Decimal | None,
    km_inicial: Decimal,
) -> EstimacionMantenimiento:
    """Próximo mantenimiento de un plan.

    - Con historial: último kilometraje realizado + intervalo.
    - Sin historial: próximo múltiplo del intervalo (p. ej. cada 10.000 km -> 10.000, 20.000, ...).
    Estado: vencido (ya pasó), próximo (faltan <= 10% del intervalo), al_día; sin_lecturas si no hay odómetro.
    """
    if ultimo_km is not None:
        proximo = ultimo_km + intervalo_km
        base = "ultimo_mantenimiento"
    else:
        referencia = km_actual if km_actual is not None else km_inicial
        multiplo = (referencia / intervalo_km).to_integral_value(rounding=ROUND_CEILING)
        proximo = max(multiplo, Decimal(1)) * intervalo_km
        base = "multiplos"

    if km_actual is None:
        return EstimacionMantenimiento(proximo, None, "sin_lecturas", base)

    restantes = proximo - km_actual
    if restantes < 0:
        estado = "vencido"
    elif restantes <= intervalo_km * UMBRAL_PROXIMO:
        estado = "proximo"
    else:
        estado = "al_dia"
    return EstimacionMantenimiento(proximo, restantes, estado, base)


_MENSAJES_ORIENTACION = {
    "sin_datos": "Todavía no hay gastos de los últimos 12 meses para orientarte.",
    "reparar": "Por ahora seguir reparando parece razonable: tus gastos no muestran señales de alerta.",
    "evaluar": "Hay una señal que conviene vigilar. Seguí registrando tus gastos para ver cómo evoluciona.",
    "considerar_reemplazo": (
        "Varias señales indican que el vehículo te está costando cada vez más. "
        "Puede ser momento de evaluar un reemplazo."
    ),
}


def evaluar_reparar_o_reemplazar(
    gasto_reparaciones_12m: Decimal,
    gasto_total_12m: Decimal,
    reparaciones_6m_recientes: Decimal,
    reparaciones_6m_previos: Decimal,
    km_actual: Decimal | None,
) -> OrientacionReparacion:
    """Orientación (no tasación) a partir de tres señales sobre los gastos propios.

    1. Peso de las reparaciones: >= 35% del gasto total de los últimos 12 meses.
    2. Reparaciones en aumento: los últimos 6 meses gastan >= 1,5 veces los 6 meses previos.
    3. Kilometraje elevado: >= 150.000 km.
    Ninguna señal -> reparar; una -> evaluar; dos o más -> considerar reemplazo.
    """
    if gasto_total_12m <= 0:
        return OrientacionReparacion("sin_datos", _MENSAJES_ORIENTACION["sin_datos"], (), AVISO_ORIENTACION)

    peso = porcentaje(gasto_reparaciones_12m, gasto_total_12m)
    senales = (
        Senal(
            "peso_reparaciones",
            f"Las reparaciones son el {peso}% de tus gastos de los últimos 12 meses "
            f"(umbral: {UMBRAL_PESO_REPARACIONES * 100:.0f}%).",
            gasto_reparaciones_12m >= gasto_total_12m * UMBRAL_PESO_REPARACIONES,
        ),
        Senal(
            "reparaciones_en_aumento",
            "El gasto en reparaciones de los últimos 6 meses es al menos "
            f"{FACTOR_AUMENTO_REPARACIONES} veces el de los 6 meses anteriores.",
            reparaciones_6m_previos > 0
            and reparaciones_6m_recientes >= reparaciones_6m_previos * FACTOR_AUMENTO_REPARACIONES,
        ),
        Senal(
            "kilometraje_elevado",
            f"El vehículo supera los {KM_ELEVADO:,.0f} km.",
            km_actual is not None and km_actual >= KM_ELEVADO,
        ),
    )

    cumplidas = sum(1 for senal in senales if senal.cumplida)
    estado = "reparar" if cumplidas == 0 else "evaluar" if cumplidas == 1 else "considerar_reemplazo"
    return OrientacionReparacion(estado, _MENSAJES_ORIENTACION[estado], senales, AVISO_ORIENTACION)
