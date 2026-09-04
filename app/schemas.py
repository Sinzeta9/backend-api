from pydantic import BaseModel


class PruebaCreate(BaseModel):
    nombre: str

class PruebaUpdate(BaseModel):
    nombre: str

class PruebaResponse(BaseModel):
    id: int
    nombre: str

class PruebaListResponse(BaseModel):
    pruebas: list[PruebaResponse]

class PruebaDeleteResponse(BaseModel):
    id: int
    nombre: str
    mensaje: str