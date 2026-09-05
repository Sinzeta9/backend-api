from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()

def crear_prueba(nombre: str):
    with engine.begin() as connection:
        result = connection.execute(
            text("INSERT INTO prueba (nombre) VALUES (:nombre) RETURNING id, nombre"),
            {"nombre": nombre},
        )
        return result.mappings().one()

def listar_pruebas():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, nombre FROM prueba ORDER BY id")
        )
        return result.mappings().all()

def actualizar_prueba(id: int, nombre: str):
    with engine.begin() as connection:
        result = connection.execute(
            text(
                "UPDATE prueba "
                "SET nombre = :nombre "
                "WHERE id = :id "
                "RETURNING id, nombre"
            ),
            {"id": id, "nombre": nombre},
        )
        return result.mappings().one_or_none()

def eliminar_prueba(id: int):
    with engine.begin() as connection:
        result = connection.execute(
            text(
                "DELETE FROM prueba "
                "WHERE id = :id "
                "RETURNING id, nombre"
            ),
            {"id": id},
        )
        return result.mappings().one_or_none()