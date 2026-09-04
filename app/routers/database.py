from fastapi import APIRouter

from app.database import crear_prueba, listar_pruebas, test_connection
from app.schemas import PruebaCreate

router = APIRouter()


@router.get("/db-test")
def db_test():
    nombre = test_connection()
    return {"database": nombre}

@router.post("/prueba")
def crear_prueba_endpoint(datos: PruebaCreate):
    resultado = crear_prueba(datos.nombre)
    return {"id": resultado["id"], "nombre": resultado["nombre"]}

@router.get("/pruebas")
def listar_pruebas_endpoint():
    pruebas = listar_pruebas()
    return {"pruebas": pruebas}