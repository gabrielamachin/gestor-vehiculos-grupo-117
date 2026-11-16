"""Recrea el esquema completo (database/schema.sql) en la base indicada por DATABASE_URL.

BORRA TODAS LAS TABLAS. Se usa para preparar la base de las pruebas E2E (frontend/e2e), por eso se
niega a actuar sobre una base cuyo nombre no contenga "e2e" o "test".

    python -m scripts.reiniciar_bd        # desde backend/, con DATABASE_URL apuntando a la base de pruebas
"""
from pathlib import Path

from app.core.database import engine

ESQUEMA = Path(__file__).resolve().parents[2] / "database" / "schema.sql"


def main() -> None:
    nombre = engine.url.database or ""
    if not any(marca in nombre.lower() for marca in ("e2e", "test")):
        raise SystemExit(
            f"Por seguridad solo se reinicia una base cuyo nombre contenga 'e2e' o 'test' (la actual es '{nombre}')."
        )

    print(f"Reiniciando el esquema en: {engine.url.render_as_string(hide_password=True)}")
    conexion = engine.raw_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute(ESQUEMA.read_text(encoding="utf-8"))  # el script trae su propio BEGIN/COMMIT
        conexion.commit()
        cursor.close()
    finally:
        conexion.close()
    print("Esquema recreado.")


if __name__ == "__main__":
    main()
