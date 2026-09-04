from pydantic import BaseModel, Field


class PruebaCreate(BaseModel):
    nombre: str = Field(min_length=1)


class PruebaUpdate(BaseModel):
    nombre: str = Field(min_length=1)

class PruebaResponse(BaseModel):
    id: int
    nombre: str

class PruebaListResponse(BaseModel):
    pruebas: list[PruebaResponse]

class PruebaDeleteResponse(BaseModel):
    id: int
    nombre: str
    mensaje: str