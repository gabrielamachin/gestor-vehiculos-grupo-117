import os

# Deben definirse antes de importar la app. Los tests de esta etapa no usan la base de datos.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "secreto-de-prueba-con-mas-de-32-caracteres!!")
