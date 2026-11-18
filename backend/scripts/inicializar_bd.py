"""Inicializa el esquema una sola vez al desplegar en Render.

No reemplaza ni borra tablas existentes. El script DDL completo solo se ejecuta
cuando la base no contiene todavía la tabla principal `usuarios`.
"""
from pathlib import Path

from sqlalchemy import inspect

from app.core.database import engine

ESQUEMA = Path(__file__).resolve().parents[2] / "database" / "schema.sql"


def main() -> None:
    inspector = inspect(engine)
    if "usuarios" in inspector.get_table_names():
        print("Esquema existente detectado; no se aplican cambios.")
        return

    print("Inicializando el esquema de PostgreSQL...")
    conexion = engine.raw_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute(ESQUEMA.read_text(encoding="utf-8"))
        conexion.commit()
        cursor.close()
    finally:
        conexion.close()
    print("Esquema creado.")


if __name__ == "__main__":
    main()
