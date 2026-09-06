from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    field_validator,
)


class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    nombre: str


class CategoriaListResponse(BaseModel):
    categorias: list[CategoriaResponse]


class PruebaCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    categoria_id: int | None = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(
        cls,
        value: str,
    ) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")

        return value


class PruebaUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None
    categoria_id: int | None = None

    @field_validator("nombre")
    @classmethod
    def validar_nombre(
        cls,
        value: str,
    ) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío")

        return value


class PruebaResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    nombre: str
    descripcion: str | None
    categoria_id: int | None


class PruebaListResponse(BaseModel):
    items: list[PruebaResponse]
    pagina: int
    tamano: int
    total: int
    paginas: int


class PruebasCategoriaResponse(BaseModel):
    pruebas: list[PruebaResponse]


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    nombre: str
    email: EmailStr
    rol: str


class UsuarioListResponse(BaseModel):
    usuarios: list[UsuarioResponse]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
