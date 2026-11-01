import uuid
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import get_settings
from app.core.errors import NoAutenticado
from app.core.security import (
    crear_token,
    decodificar_token,
    hashear_password,
    verificar_password,
)


def test_password_se_hashea_y_se_verifica():
    h = hashear_password("clave-segura-123")
    assert h != "clave-segura-123"
    assert verificar_password("clave-segura-123", h)
    assert not verificar_password("otra-clave", h)


def test_password_de_mas_de_72_bytes_no_rompe_la_verificacion():
    h = hashear_password("clave-segura-123")
    assert verificar_password("x" * 100, h) is False


def test_token_ida_y_vuelta():
    usuario_id = uuid.uuid4()
    assert decodificar_token(crear_token(usuario_id)) == usuario_id


def test_token_con_otra_firma_se_rechaza():
    token = jwt.encode({"sub": str(uuid.uuid4())}, "otra-clave-distinta-de-32-caracteres-!!", algorithm="HS256")
    with pytest.raises(NoAutenticado):
        decodificar_token(token)


def test_token_vencido_se_rechaza():
    s = get_settings()
    payload = {"sub": str(uuid.uuid4()), "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
    token = jwt.encode(payload, s.jwt_secret, algorithm=s.jwt_algorithm)
    with pytest.raises(NoAutenticado):
        decodificar_token(token)


def test_token_sin_sub_se_rechaza():
    s = get_settings()
    token = jwt.encode({"exp": datetime.now(timezone.utc) + timedelta(minutes=5)}, s.jwt_secret, algorithm=s.jwt_algorithm)
    with pytest.raises(NoAutenticado):
        decodificar_token(token)
