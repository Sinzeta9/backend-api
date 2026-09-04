from pydantic import BaseModel


class PruebaCreate(BaseModel):
    nombre: str

class PruebaUpdate(BaseModel):
    nombre: str