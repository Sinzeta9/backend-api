from typing import Annotated
from pydantic import BaseModel, StringConstraints


NombreValido = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
    ),
]

class PruebaCreate(BaseModel):
    nombre: NombreValido


class PruebaUpdate(BaseModel):
    nombre: NombreValido

class PruebaResponse(BaseModel):
    id: int
    nombre: str

class PruebaListResponse(BaseModel):
    pruebas: list[PruebaResponse]

class PruebaDeleteResponse(BaseModel):
    id: int
    nombre: str
    mensaje: str