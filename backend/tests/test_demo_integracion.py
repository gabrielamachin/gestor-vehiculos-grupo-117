"""Verifica que los datos de demo disparan cada indicador, contra una PostgreSQL real."""
import pytest

from scripts import cargar_datos_demo as demo
from tests.utils_integracion import SALTAR_SIN_BASE, cliente_de_prueba, sesion_de_prueba

pytestmark = SALTAR_SIN_BASE


@pytest.fixture(scope="module")
def client():
    yield from cliente_de_prueba()


def _entrar(client) -> dict:
    r = client.post("/usuarios/login", json={"email": demo.EMAIL_DEMO, "password": demo.PASSWORD_DEMO})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _resumenes(client, headers) -> dict:
    vehiculos = {v["alias"]: v["id"] for v in client.get("/vehiculos", headers=headers).json()}
    assert set(vehiculos) == {"Toyota Corolla", "Ford Fiesta", "Moto Honda"}
    return {
        alias: client.get(f"/indicadores/vehiculos/{vid}/resumen", headers=headers).json()
        for alias, vid in vehiculos.items()
    }


def test_los_datos_de_demo_disparan_los_indicadores(client):
    with sesion_de_prueba(client) as db:
        assert demo.cargar(db)["vehiculos"] == 3
    r = _resumenes(client, _entrar(client))

    corolla = r["Toyota Corolla"]
    assert corolla["costo_por_km"]["estado"] == "ok"
    assert corolla["alerta_combustible"]["estado"] == "alerta"
    assert corolla["alerta_combustible"]["desvio_pct"] > 40
    assert {p["nombre"]: p["estado"] for p in corolla["proximos_mantenimientos"]} == {
        "Cambio de aceite": "proximo",
        "Filtros": "al_dia",
        "Correa de distribución": "vencido",
        "Frenos": "al_dia",
    }
    assert corolla["proximos_mantenimientos"][0]["nombre"] == "Correa de distribución"   # lo más urgente primero
    assert corolla["reparar_o_reemplazar"]["estado"] == "reparar"
    assert corolla["gasto_por_categoria"]["total_fijo"] > 0

    fiesta = r["Ford Fiesta"]
    assert fiesta["alerta_combustible"]["estado"] == "normal"
    assert fiesta["reparar_o_reemplazar"]["estado"] == "considerar_reemplazo"
    assert all(s["cumplida"] for s in fiesta["reparar_o_reemplazar"]["senales"])

    moto = r["Moto Honda"]
    assert moto["costo_por_km"]["estado"] == "sin_lecturas"
    assert moto["alerta_combustible"]["estado"] == "sin_datos"
    assert moto["proximos_mantenimientos"] == []
    assert moto["reparar_o_reemplazar"]["estado"] == "sin_datos"


def test_cargar_dos_veces_exige_reiniciar(client):
    with sesion_de_prueba(client) as db:
        with pytest.raises(ValueError, match="--reiniciar"):
            demo.cargar(db)
        demo.cargar(db, reiniciar=True)
    assert len(client.get("/vehiculos", headers=_entrar(client)).json()) == 3   # recreado, sin duplicar
