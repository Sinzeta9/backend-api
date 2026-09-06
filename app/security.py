from datetime import datetime, timedelta, timezone

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.config import (
    JWT_ALGORITHM,
    JWT_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)

password_hash = PasswordHash.recommended()


def crear_hash_password(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(
    password: str,
    password_guardado: str,
) -> bool:
    return password_hash.verify(
        password,
        password_guardado,
    )


def crear_access_token(
    usuario_id: int,
) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(usuario_id),
        "exp": expiracion,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decodificar_access_token(
    token: str,
) -> int | None:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            return None

        return int(usuario_id)

    except (InvalidTokenError, ValueError):
        return None
