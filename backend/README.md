# Backend — Gestor Inteligente de Vehículos

API REST con FastAPI. Estructura y reglas de dependencia: [docs/arquitectura.md](../docs/arquitectura.md) (sección 1.4).

## Puesta en marcha local

Desde la carpeta `backend/`:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env               # completar DATABASE_URL y JWT_SECRET

createdb gestor_vehiculos          # o crear la base desde pgAdmin
psql -d gestor_vehiculos -f ../database/schema.sql

uvicorn app.main:app --reload
```

- Documentación interactiva (Swagger): http://localhost:8000/docs
- Salud de la API: `GET /health` · conexión con la base: `GET /health/db`

Para probar endpoints protegidos en Swagger: hacer `POST /usuarios/login`, copiar el `access_token`, botón **Authorize** y pegarlo.

## Tests

```bash
pytest
```

Las pruebas de integración usan una base de datos PostgreSQL de prueba y se saltean si no está definida `TEST_DATABASE_URL`. Usar una base exclusiva (por ejemplo `gestor_vehiculos_test`): cada corrida ejecuta `schema.sql`, que **borra y recrea las tablas**.

```powershell
$env:TEST_DATABASE_URL="postgresql://postgres:TU_CLAVE@localhost:5432/gestor_vehiculos_test"
pytest
```

## Convenciones al agregar un módulo

1. Crear `app/<modulo>/` con `router.py`, `schemas.py`, `service.py`, `repository.py` y `models.py` (tomar `usuarios/` como molde).
2. Registrar el router en `app/main.py`.
3. El servicio es quien hace `commit`; el repositorio solo hace `flush`.
4. Un módulo accede solo a sus tablas. Para datos de otro módulo, usar el **service** de ese módulo.
5. Los servicios lanzan errores de `app/core/errors.py`; nunca `HTTPException`.
