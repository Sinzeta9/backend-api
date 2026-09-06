from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

NombreValido = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
    ),
]


class CategoriaCreate(BaseModel):
    nombre: NombreValido


class CategoriaResponse(BaseModel):
    id: int
    nombre: str


class CategoriaListResponse(BaseModel):
    categorias: list[CategoriaResponse]


class PruebaCreate(BaseModel):
    nombre: NombreValido
    descripcion: str | None = None
    categoria_id: int | None = None


class PruebaUpdate(BaseModel):
    nombre: NombreValido
    descripcion: str | None = None
    categoria_id: int | None = None


class PruebaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    categoria_id: int | None


class PruebaListResponse(BaseModel):
    pruebas: list[PruebaResponse]


class UsuarioCreate(BaseModel):
    nombre: NombreValido
    email: EmailStr
    password: str


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr


class UsuarioListResponse(BaseModel):
    usuarios: list[UsuarioResponse]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
