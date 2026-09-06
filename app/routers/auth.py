from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import LoginRequest, TokenResponse, UsuarioResponse
from app.security import (
    crear_access_token,
    decodificar_access_token,
    verificar_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

DatabaseDependency = Annotated[
    Session,
    Depends(get_db),
]

bearer_scheme = HTTPBearer(
    auto_error=False,
)

BearerDependency = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


def obtener_usuario_actual(
    credenciales: BearerDependency,
    db: DatabaseDependency,
):
    if credenciales is None:
        raise HTTPException(
            status_code=401,
            detail="No autenticado",
        )

    usuario_id = decodificar_access_token(
        credenciales.credentials,
    )

    if usuario_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
        )

    usuario = db.get(
        Usuario,
        usuario_id,
    )

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
        )

    return usuario


UsuarioActualDependency = Annotated[
    Usuario,
    Depends(obtener_usuario_actual),
]


def requerir_admin(
    usuario: UsuarioActualDependency,
):
    if usuario.rol != "admin":
        raise HTTPException(
            status_code=403,
            detail="Permisos insuficientes",
        )

    return usuario


AdminDependency = Annotated[
    Usuario,
    Depends(requerir_admin),
]


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    datos: LoginRequest,
    db: DatabaseDependency,
):
    usuario = db.scalar(
        select(Usuario).where(
            Usuario.email == datos.email,
        )
    )

    if usuario is None or not verificar_password(
        datos.password,
        usuario.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas",
        )

    access_token = crear_access_token(
        usuario.id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UsuarioResponse,
)
def usuario_actual(
    usuario: UsuarioActualDependency,
):
    return usuario
