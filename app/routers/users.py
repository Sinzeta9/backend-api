from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.routers.auth import AdminDependency
from app.schemas import (
    UsuarioCreate,
    UsuarioListResponse,
    UsuarioResponse,
)
from app.security import crear_hash_password

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)

DatabaseDependency = Annotated[
    Session,
    Depends(get_db),
]


@router.post(
    "",
    response_model=UsuarioResponse,
    status_code=201,
)
def crear_usuario(
    datos: UsuarioCreate,
    db: DatabaseDependency,
):
    usuario_existente = db.scalar(
        select(Usuario).where(
            Usuario.email == datos.email,
        )
    )

    if usuario_existente is not None:
        raise HTTPException(
            status_code=409,
            detail="El email ya está registrado",
        )

    usuario = Usuario(
        nombre=datos.nombre,
        email=str(datos.email),
        password_hash=crear_hash_password(
            datos.password,
        ),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.get(
    "",
    response_model=UsuarioListResponse,
)
def listar_usuarios(
    db: DatabaseDependency,
    admin: AdminDependency,
):
    usuarios = db.scalars(select(Usuario).order_by(Usuario.id)).all()

    return {
        "usuarios": usuarios,
    }


@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
)
def obtener_usuario(
    usuario_id: int,
    db: DatabaseDependency,
):
    usuario = db.get(
        Usuario,
        usuario_id,
    )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado",
        )

    return usuario
