from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.models import Prueba

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()


def crear_prueba(db, nombre: str):
    prueba = Prueba(nombre=nombre)

    db.add(prueba)
    db.commit()
    db.refresh(prueba)

    return {
        "id": prueba.id,
        "nombre": prueba.nombre,
    }


def listar_pruebas(db):
    pruebas = db.scalars(select(Prueba).order_by(Prueba.id)).all()

    return [{"id": prueba.id, "nombre": prueba.nombre} for prueba in pruebas]


def actualizar_prueba(db, id: int, nombre: str):
    prueba = db.get(Prueba, id)

    if prueba is None:
        return None

    prueba.nombre = nombre

    db.commit()
    db.refresh(prueba)

    return {
        "id": prueba.id,
        "nombre": prueba.nombre,
    }


def eliminar_prueba(db, id: int):
    prueba = db.get(Prueba, id)

    if prueba is None:
        return None

    resultado = {
        "id": prueba.id,
        "nombre": prueba.nombre,
    }

    db.delete(prueba)
    db.commit()

    return resultado
