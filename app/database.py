import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT nombre FROM prueba WHERE id = 1"))
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