from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    actualizar_prueba,
    crear_prueba,
    eliminar_prueba,
    get_db,
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

DatabaseDependency = Annotated[Session, Depends(get_db)]


@router.get("/db-test")
def db_test():
    nombre = test_connection()
    return {"database": nombre}


@router.post(
    "/prueba",
    response_model=PruebaResponse,
    status_code=201,
)
def crear_prueba_endpoint(
    datos: PruebaCreate,
    db: DatabaseDependency,
):
    resultado = crear_prueba(db, datos.nombre)

    return {
        "id": resultado["id"],
        "nombre": resultado["nombre"],
    }


@router.get("/pruebas", response_model=PruebaListResponse)
def listar_pruebas_endpoint(db: DatabaseDependency):
    pruebas = listar_pruebas(db)

    return {"pruebas": pruebas}


@router.put("/prueba/{id}", response_model=PruebaResponse)
def actualizar_prueba_endpoint(
    id: int,
    datos: PruebaUpdate,
    db: DatabaseDependency,
):
    resultado = actualizar_prueba(db, id, datos.nombre)

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
def eliminar_prueba_endpoint(
    id: int,
    db: DatabaseDependency,
):
    resultado = eliminar_prueba(db, id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado",
        )
