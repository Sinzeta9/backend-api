from fastapi import APIRouter, HTTPException

from app.database import (
    actualizar_prueba,
    crear_prueba,
    eliminar_prueba,
    listar_pruebas,
    test_connection,
)

from app.schemas import (
    PruebaCreate,
    PruebaListResponse,
    PruebaResponse,
    PruebaUpdate,
)

router = APIRouter()


@router.get("/db-test")
def db_test():
    nombre = test_connection()
    return {"database": nombre}


@router.post(
    "/prueba",
    response_model=PruebaResponse,
    status_code=201,
)
def crear_prueba_endpoint(datos: PruebaCreate):
    resultado = crear_prueba(datos.nombre)

    return {
        "id": resultado["id"],
        "nombre": resultado["nombre"],
    }


@router.get("/pruebas", response_model=PruebaListResponse)
def listar_pruebas_endpoint():
    pruebas = listar_pruebas()

    return {"pruebas": pruebas}


@router.put("/prueba/{id}", response_model=PruebaResponse)
def actualizar_prueba_endpoint(id: int, datos: PruebaUpdate):
    resultado = actualizar_prueba(id, datos.nombre)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado",
        )

    return {
        "id": resultado["id"],
        "nombre": resultado["nombre"],
    }


@router.delete(
    "/prueba/{id}",
    status_code=204,
)
def eliminar_prueba_endpoint(id: int):
    resultado = eliminar_prueba(id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado",
        )
    
    return {
        "id": resultado["id"],
        "nombre": resultado["nombre"],
        "mensaje": "Registro eliminado",
    }