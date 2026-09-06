from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import (
    actualizar_prueba,
    crear_categoria,
    crear_prueba,
    eliminar_prueba,
    get_db,
    listar_categorias,
    listar_pruebas,
    listar_pruebas_categoria,
    obtener_categoria,
    test_connection,
)
from app.schemas import (
    CategoriaCreate,
    CategoriaListResponse,
    CategoriaResponse,
    PruebaCreate,
    PruebaListResponse,
    PruebaResponse,
    PruebaUpdate,
)

router = APIRouter()

DatabaseDependency = Annotated[Session, Depends(get_db)]


@router.get("/db-test")
def db_test():
    resultado = test_connection()
    return {"database": resultado}


@router.post(
    "/categorias",
    response_model=CategoriaResponse,
    status_code=201,
)
def crear_categoria_endpoint(
    datos: CategoriaCreate,
    db: DatabaseDependency,
):
    return crear_categoria(db, datos.nombre)


@router.get(
    "/categorias",
    response_model=CategoriaListResponse,
)
def listar_categorias_endpoint(
    db: DatabaseDependency,
):
    categorias = listar_categorias(db)

    return {"categorias": categorias}


@router.get(
    "/categorias/{categoria_id}/pruebas",
    response_model=PruebaListResponse,
)
def listar_pruebas_categoria_endpoint(
    categoria_id: int,
    db: DatabaseDependency,
):
    categoria = obtener_categoria(db, categoria_id)

    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada",
        )

    pruebas = listar_pruebas_categoria(
        db,
        categoria_id,
    )

    return {"pruebas": pruebas}


@router.post(
    "/prueba",
    response_model=PruebaResponse,
    status_code=201,
)
def crear_prueba_endpoint(
    datos: PruebaCreate,
    db: DatabaseDependency,
):
    if datos.categoria_id is not None:
        categoria = obtener_categoria(
            db,
            datos.categoria_id,
        )

        if categoria is None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada",
            )

    return crear_prueba(
        db,
        datos.nombre,
        datos.descripcion,
        datos.categoria_id,
    )


@router.get(
    "/pruebas",
    response_model=PruebaListResponse,
)
def listar_pruebas_endpoint(
    db: DatabaseDependency,
):
    pruebas = listar_pruebas(db)

    return {"pruebas": pruebas}


@router.put(
    "/prueba/{id}",
    response_model=PruebaResponse,
)
def actualizar_prueba_endpoint(
    id: int,
    datos: PruebaUpdate,
    db: DatabaseDependency,
):
    if datos.categoria_id is not None:
        categoria = obtener_categoria(
            db,
            datos.categoria_id,
        )

        if categoria is None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada",
            )

    resultado = actualizar_prueba(
        db,
        id,
        datos.nombre,
        datos.descripcion,
        datos.categoria_id,
    )

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado",
        )

    return resultado


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
