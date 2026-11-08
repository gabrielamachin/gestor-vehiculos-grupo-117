import os

# Deben definirse antes de importar la app. Los tests que no son de integración no usan la base de datos.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SECRET", "secreto-de-prueba-con-mas-de-32-caracteres!!")
# Las pruebas usan http://testserver: una cookie Secure no se enviaría.
os.environ.setdefault("COOKIE_SECURE", "false")
