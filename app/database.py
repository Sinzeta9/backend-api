from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.models import Prueba

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
    with SessionLocal() as db:
        pruebas = db.scalars(
            select(Prueba).order_by(Prueba.id)
        ).all()

        return [
            {"id": prueba.id, "nombre": prueba.nombre}
            for prueba in pruebas
        ]

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