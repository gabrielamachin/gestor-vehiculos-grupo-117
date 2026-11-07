"""Carga datos de demostración: un usuario con tres vehículos que ejercitan todos los indicadores.

Las fechas son relativas a HOY, por lo que los indicadores se comportan igual sin importar
cuándo se ejecute. Usa los servicios de cada módulo (mismas validaciones que la API).

Uso, desde la carpeta backend/ y con el .env apuntando a la base deseada:

    python -m scripts.cargar_datos_demo              # falla si el usuario demo ya existe
    python -m scripts.cargar_datos_demo --reiniciar  # borra al usuario demo (y todo lo suyo) y lo recrea

Usuario demo:  demo@gestor.com  /  demo1234

Qué muestra cada vehículo:
    Toyota Corolla  -> alerta de combustible; mantenimientos próximo / al día / vencido; "seguir reparando"
    Ford Fiesta     -> "considerar reemplazo" (reparaciones pesadas y en aumento, muchos km); combustible normal
    Moto Honda      -> sin datos (estados vacíos)
"""
import argparse
from datetime import date
from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.categorias import service as categorias_service
from app.core.database import SessionLocal, engine
from app.gastos import service as gastos_service
from app.gastos.schemas import GastoCrear
from app.kilometraje import service as kilometraje_service
from app.kilometraje.schemas import LecturaCrear
from app.mantenimiento import service as mantenimiento_service
from app.mantenimiento.schemas import PlanCrear
from app.usuarios import service as usuarios_service
from app.usuarios.models import Usuario
from app.usuarios.schemas import UsuarioRegistro
from app.vehiculos import service as vehiculos_service
from app.vehiculos.schemas import VehiculoCrear

EMAIL_DEMO = "demo@gestor.com"
PASSWORD_DEMO = "demo1234"
CODIGOS = ("combustible", "mantenimiento", "reparacion", "seguro")


def _fecha(hoy: date, meses_atras: int, dia: int) -> date:
    """Día `dia` del mes que está `meses_atras` meses antes de hoy (siempre en el pasado si meses_atras >= 1)."""
    anio, mes0 = divmod(hoy.year * 12 + hoy.month - 1 - meses_atras, 12)
    return date(anio, mes0 + 1, dia)


class _Carga:
    """Atajos para cargar datos de un usuario a través de los servicios."""

    def __init__(self, db: Session, usuario_id, categorias: dict, hoy: date):
        self.db, self.usuario_id, self.categorias, self.hoy = db, usuario_id, categorias, hoy

    def vehiculo(self, alias: str, km_inicial: int):
        return vehiculos_service.crear(
            self.db, self.usuario_id, VehiculoCrear(alias=alias, kilometraje_inicial=Decimal(km_inicial))
        )

    def lectura(self, vehiculo, meses_atras: int, km: int) -> None:
        datos = LecturaCrear(vehiculo_id=vehiculo.id, fecha=_fecha(self.hoy, meses_atras, 20), kilometraje=Decimal(km))
        kilometraje_service.crear(self.db, self.usuario_id, datos)

    def plan(self, vehiculo, nombre: str, intervalo_km: int):
        datos = PlanCrear(vehiculo_id=vehiculo.id, nombre=nombre, intervalo_km=Decimal(intervalo_km))
        return mantenimiento_service.crear(self.db, self.usuario_id, datos)

    def gasto(self, vehiculo, codigo: str, meses_atras: int, monto: int, dia: int = 12, descripcion=None, plan=None, km=None):
        datos = GastoCrear(
            vehiculo_id=vehiculo.id,
            categoria_id=self.categorias[codigo].id,
            plan_mantenimiento_id=plan.id if plan is not None else None,
            monto=Decimal(monto),
            fecha=_fecha(self.hoy, meses_atras, dia),
            kilometraje=Decimal(km) if km is not None else None,
            descripcion=descripcion,
        )
        gastos_service.crear(self.db, self.usuario_id, datos)


def _toyota_corolla(c: _Carga) -> None:
    v = c.vehiculo("Toyota Corolla", 30000)
    for meses, km in [(6, 44000), (5, 46000), (4, 48000), (3, 49500), (2, 51000), (1, 52500)]:
        c.lectura(v, meses, km)

    # Combustible estable y un último mes 45% más alto -> alerta
    for meses, monto in [(6, 40000), (5, 41000), (4, 39500), (3, 40500), (2, 40000), (1, 58000)]:
        c.gasto(v, "combustible", meses, monto, descripcion="Carga de combustible")
    for meses in range(1, 6):
        c.gasto(v, "seguro", meses, 15000, dia=5, descripcion="Cuota del seguro")
    c.gasto(v, "reparacion", 3, 12000, descripcion="Cambio de batería")

    # Planes: aceite (próximo), filtros (al día), correa (vencido), frenos (sin historial)
    aceite, filtros = c.plan(v, "Cambio de aceite", 10000), c.plan(v, "Filtros", 20000)
    correa, _frenos = c.plan(v, "Correa de distribución", 15000), c.plan(v, "Frenos", 30000)
    c.gasto(v, "mantenimiento", 7, 45000, plan=aceite, km=43000, descripcion="Aceite y filtro")
    c.gasto(v, "mantenimiento", 10, 38000, plan=filtros, km=35000, descripcion="Filtros de aire y habitáculo")
    c.gasto(v, "mantenimiento", 9, 52000, plan=correa, km=36000, descripcion="Correa y tensor")


def _ford_fiesta(c: _Carga) -> None:
    v = c.vehiculo("Ford Fiesta", 150000)
    for meses, km in [(11, 152000), (6, 160000), (1, 168000)]:
        c.lectura(v, meses, km)

    for meses in range(1, 12):
        c.gasto(v, "combustible", meses, 10000, descripcion="Carga de combustible")
    # Reparaciones: 30.000 en el semestre anterior, 80.000 en los últimos 6 meses
    c.gasto(v, "reparacion", 9, 30000, descripcion="Embrague")
    c.gasto(v, "reparacion", 4, 45000, descripcion="Caja de cambios")
    c.gasto(v, "reparacion", 2, 35000, descripcion="Tren delantero")


def _moto_honda(c: _Carga) -> None:
    c.vehiculo("Moto Honda", 0)  # sin lecturas, gastos ni planes: muestra los estados vacíos


def cargar(db: Session, hoy: date | None = None, reiniciar: bool = False) -> dict:
    """Crea el usuario demo y sus datos. Con `reiniciar`, borra antes al usuario demo (y todo lo suyo)."""
    hoy = hoy or date.today()

    if db.scalar(select(Usuario).where(Usuario.email == EMAIL_DEMO)) is not None:
        if not reiniciar:
            raise ValueError(f"El usuario {EMAIL_DEMO} ya existe. Usar --reiniciar para borrarlo y recrearlo.")
        db.execute(delete(Usuario).where(Usuario.email == EMAIL_DEMO))  # ON DELETE CASCADE borra todo lo suyo
        db.commit()

    categorias = {codigo: categorias_service.obtener_por_codigo(db, codigo) for codigo in CODIGOS}
    faltantes = [codigo for codigo, categoria in categorias.items() if categoria is None]
    if faltantes:
        raise ValueError(f"Faltan categorías en la base ({', '.join(faltantes)}). Ejecutar database/schema.sql.")

    usuario = usuarios_service.registrar(
        db, UsuarioRegistro(nombre="Usuario Demo", email=EMAIL_DEMO, password=PASSWORD_DEMO)
    )
    carga = _Carga(db, usuario.id, categorias, hoy)
    _toyota_corolla(carga)
    _ford_fiesta(carga)
    _moto_honda(carga)
    return {"email": EMAIL_DEMO, "password": PASSWORD_DEMO, "vehiculos": 3}


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga el usuario y los datos de demostración.")
    parser.add_argument("--reiniciar", action="store_true", help="borra al usuario demo y lo recrea")
    args = parser.parse_args()

    print(f"Base de datos: {engine.url.render_as_string(hide_password=True)}")
    with SessionLocal() as db:
        try:
            resultado = cargar(db, reiniciar=args.reiniciar)
        except ValueError as error:
            raise SystemExit(str(error))
    print(f"Listo: {resultado['vehiculos']} vehículos cargados. Ingresar con {resultado['email']} / {resultado['password']}")


if __name__ == "__main__":
    main()
