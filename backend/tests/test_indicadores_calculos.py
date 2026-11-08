"""Pruebas de las fórmulas de Indicadores (funciones puras: sin base de datos ni FastAPI)."""
from datetime import date
from decimal import Decimal as D

import pytest

from app.indicadores import calculos


def _meses(*totales, anio=2024):
    """Serie mensual de prueba: un total por mes consecutivo desde enero."""
    return [(date(anio, i + 1, 1), D(t)) for i, t in enumerate(totales)]


# ---------- porcentaje ----------

def test_porcentaje():
    assert calculos.porcentaje(D("25"), D("200")) == D("12.50")
    assert calculos.porcentaje(D("1"), D("3")) == D("33.33")


def test_porcentaje_con_total_cero_es_cero():
    assert calculos.porcentaje(D("0"), D("0")) == D("0.00")


# ---------- costo por km ----------

def test_costo_por_km():
    r = calculos.costo_por_km(D("50000"), km_inicial=D("1000"), km_actual=D("11000"))
    assert r.estado == "ok"
    assert r.costo_por_km == D("5.00")
    assert r.km_recorridos == D("10000")
    assert r.total_gastado == D("50000")


def test_costo_por_km_redondea_a_dos_decimales():
    r = calculos.costo_por_km(D("100"), km_inicial=D("0"), km_actual=D("3"))
    assert r.costo_por_km == D("33.33")


def test_costo_por_km_sin_gastos_es_cero():
    r = calculos.costo_por_km(D("0"), km_inicial=D("0"), km_actual=D("500"))
    assert r.estado == "ok" and r.costo_por_km == D("0.00")


def test_costo_por_km_sin_lecturas():
    r = calculos.costo_por_km(D("50000"), km_inicial=D("1000"), km_actual=None)
    assert r.estado == "sin_lecturas"
    assert r.costo_por_km is None
    assert r.total_gastado == D("50000")


@pytest.mark.parametrize("actual", [D("1000"), D("900")])
def test_costo_por_km_sin_recorrido(actual):
    r = calculos.costo_por_km(D("50000"), km_inicial=D("1000"), km_actual=actual)
    assert r.estado == "sin_recorrido"
    assert r.costo_por_km is None


# ---------- alerta de combustible ----------

def test_combustible_sin_datos():
    r = calculos.evaluar_combustible([])
    assert r.estado == "sin_datos"
    assert r.mes_evaluado is None and r.promedio_historico is None


def test_combustible_historial_insuficiente():
    r = calculos.evaluar_combustible(_meses(100, 100, 500))  # solo 2 meses previos
    assert r.estado == "historial_insuficiente"
    assert r.meses_en_historial == 2
    assert r.gasto_mes == D("500")
    assert r.promedio_historico is None


def test_combustible_normal():
    r = calculos.evaluar_combustible(_meses(100, 100, 100, 110))
    assert r.estado == "normal"
    assert r.promedio_historico == D("100.00")
    assert r.desvio_pct == D("10.00")


def test_combustible_alerta():
    r = calculos.evaluar_combustible(_meses(100, 100, 100, 150))
    assert r.estado == "alerta"
    assert r.mes_evaluado == date(2024, 4, 1)
    assert r.gasto_mes == D("150")
    assert r.promedio_historico == D("100.00")
    assert r.desvio_pct == D("50.00")
    assert r.umbral_pct == D("20.00")


def test_combustible_justo_en_el_umbral_es_alerta():
    assert calculos.evaluar_combustible(_meses(100, 100, 100, 120)).estado == "alerta"


def test_combustible_justo_debajo_del_umbral_es_normal():
    assert calculos.evaluar_combustible(_meses(100, 100, 100, 119)).estado == "normal"


def test_combustible_mes_mas_bajo_que_el_promedio_es_normal():
    r = calculos.evaluar_combustible(_meses(100, 100, 100, 50))
    assert r.estado == "normal"
    assert r.desvio_pct == D("-50.00")


def test_combustible_ordena_la_serie_recibida():
    desordenada = [(date(2024, 4, 1), D("150")), (date(2024, 1, 1), D("100")), (date(2024, 3, 1), D("100")), (date(2024, 2, 1), D("100"))]
    r = calculos.evaluar_combustible(desordenada)
    assert r.estado == "alerta" and r.mes_evaluado == date(2024, 4, 1)


def test_combustible_promedia_solo_meses_con_gasto():
    # Enero, marzo, mayo y junio: los meses sin cargas no cuentan como 0 en el promedio.
    serie = [(date(2024, 1, 1), D("100")), (date(2024, 3, 1), D("100")), (date(2024, 5, 1), D("100")), (date(2024, 6, 1), D("100"))]
    r = calculos.evaluar_combustible(serie)
    assert r.meses_en_historial == 3
    assert r.promedio_historico == D("100.00")
    assert r.estado == "normal"


# ---------- próximo mantenimiento ----------

def test_proximo_con_historial_al_dia():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=D("20000"), km_actual=D("25000"), km_inicial=D("0"))
    assert (r.proximo_km, r.km_restantes, r.estado, r.base) == (D("30000"), D("5000"), "al_dia", "ultimo_mantenimiento")


def test_proximo_cuando_faltan_menos_del_10_por_ciento_del_intervalo():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=D("20000"), km_actual=D("29000"), km_inicial=D("0"))
    assert r.estado == "proximo" and r.km_restantes == D("1000")  # justo en el límite (10% de 10.000)


def test_vencido_cuando_se_paso_del_kilometraje():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=D("20000"), km_actual=D("30500"), km_inicial=D("0"))
    assert r.estado == "vencido" and r.km_restantes == D("-500")


def test_justo_en_el_kilometraje_toca_ahora_y_no_esta_vencido():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=D("20000"), km_actual=D("30000"), km_inicial=D("0"))
    assert r.estado == "proximo" and r.km_restantes == D("0")


def test_sin_historial_usa_el_proximo_multiplo_del_intervalo():
    r = calculos.estimar_proximo_mantenimiento(D("30000"), ultimo_km=None, km_actual=D("52500"), km_inicial=D("30000"))
    assert (r.proximo_km, r.km_restantes, r.estado, r.base) == (D("60000"), D("7500"), "al_dia", "multiplos")


def test_sin_historial_y_justo_en_un_multiplo_toca_ahora():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=None, km_actual=D("30000"), km_inicial=D("0"))
    assert r.proximo_km == D("30000") and r.estado == "proximo"


def test_sin_historial_con_odometro_en_cero_el_primero_es_el_intervalo():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=None, km_actual=D("0"), km_inicial=D("0"))
    assert r.proximo_km == D("10000")


def test_sin_lecturas_estima_pero_no_calcula_restantes():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=D("20000"), km_actual=None, km_inicial=D("0"))
    assert (r.proximo_km, r.km_restantes, r.estado) == (D("30000"), None, "sin_lecturas")


def test_sin_lecturas_y_sin_historial_usa_el_kilometraje_inicial_como_referencia():
    r = calculos.estimar_proximo_mantenimiento(D("10000"), ultimo_km=None, km_actual=None, km_inicial=D("42000"))
    assert r.proximo_km == D("50000") and r.estado == "sin_lecturas"


# ---------- reparar o reemplazar ----------

def _evaluar(rep_12m, total_12m, recientes, previos, km):
    return calculos.evaluar_reparar_o_reemplazar(D(rep_12m), D(total_12m), D(recientes), D(previos), None if km is None else D(km))


def _cumplidas(r):
    return {s.codigo for s in r.senales if s.cumplida}


def test_reparar_sin_gastos_es_sin_datos():
    r = _evaluar(0, 0, 0, 0, 80000)
    assert r.estado == "sin_datos" and r.senales == ()
    assert r.aviso  # siempre aclara que no es una tasación


def test_reparar_si_no_hay_senales():
    r = _evaluar(10000, 100000, 5000, 5000, 80000)
    assert r.estado == "reparar"
    assert _cumplidas(r) == set()
    assert len(r.senales) == 3


def test_evaluar_con_una_sola_senal():
    r = _evaluar(10000, 100000, 5000, 5000, 160000)  # solo kilometraje elevado
    assert r.estado == "evaluar"
    assert _cumplidas(r) == {"kilometraje_elevado"}


def test_considerar_reemplazo_con_dos_senales():
    r = _evaluar(50000, 100000, 5000, 5000, 160000)  # peso 50% + kilometraje
    assert r.estado == "considerar_reemplazo"
    assert _cumplidas(r) == {"peso_reparaciones", "kilometraje_elevado"}


def test_considerar_reemplazo_con_las_tres_senales():
    r = _evaluar(110000, 220000, 80000, 30000, 168000)
    assert r.estado == "considerar_reemplazo"
    assert _cumplidas(r) == {"peso_reparaciones", "reparaciones_en_aumento", "kilometraje_elevado"}


def test_peso_justo_en_el_umbral_cuenta():
    assert "peso_reparaciones" in _cumplidas(_evaluar(35000, 100000, 0, 0, None))
    assert "peso_reparaciones" not in _cumplidas(_evaluar(34999, 100000, 0, 0, None))


def test_aumento_justo_en_el_factor_cuenta():
    resultado = _evaluar(0, 1, 16000, 10000, None)
    assert "reparaciones_en_aumento" in _cumplidas(resultado)
    descripcion = next(s.descripcion for s in resultado.senales if s.codigo == "reparaciones_en_aumento")
    assert "1,6 veces" in descripcion
    assert "reparaciones_en_aumento" not in _cumplidas(_evaluar(0, 1, 15999, 10000, None))


def test_aumento_no_se_evalua_si_antes_no_habia_reparaciones():
    # Sin reparaciones previas no hay base de comparación: una primera reparación no es "aumento".
    assert "reparaciones_en_aumento" not in _cumplidas(_evaluar(0, 1, 50000, 0, None))


def test_kilometraje_desconocido_no_cumple_la_senal():
    assert "kilometraje_elevado" not in _cumplidas(_evaluar(0, 1, 0, 0, None))


def test_kilometraje_elevado_usa_separador_de_miles_local():
    resultado = _evaluar(0, 1, 0, 0, 150000)
    senal = next(s for s in resultado.senales if s.codigo == "kilometraje_elevado")
    assert senal.descripcion == "El vehículo supera los 150.000 km."
    assert senal.cumplida
