from collections.abc import Generator

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import DATABASE_URL
from app.models import Categoria, Prueba

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db


def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()


def crear_categoria(db: Session, nombre: str):
    categoria = Categoria(nombre=nombre)

    db.add(categoria)
    db.commit()
    db.refresh(categoria)

    return categoria


def listar_categorias(db: Session):
    return db.scalars(select(Categoria).order_by(Categoria.id)).all()


def obtener_categoria(db: Session, categoria_id: int):
    return db.get(Categoria, categoria_id)


def listar_pruebas_categoria(
    db: Session,
    categoria_id: int,
):
    return db.scalars(
        select(Prueba).where(Prueba.categoria_id == categoria_id).order_by(Prueba.id)
    ).all()


def crear_prueba(
    db: Session,
    nombre: str,
    descripcion: str | None,
    categoria_id: int | None,
):
    prueba = Prueba(
        nombre=nombre,
        descripcion=descripcion,
        categoria_id=categoria_id,
    )

    db.add(prueba)
    db.commit()
    db.refresh(prueba)

    return prueba


def listar_pruebas(db: Session):
    return db.scalars(select(Prueba).order_by(Prueba.id)).all()


def actualizar_prueba(
    db: Session,
    id: int,
    nombre: str,
    descripcion: str | None,
    categoria_id: int | None,
):
    prueba = db.get(Prueba, id)

    if prueba is None:
        return None

    prueba.nombre = nombre
    prueba.descripcion = descripcion
    prueba.categoria_id = categoria_id

    db.commit()
    db.refresh(prueba)

    return prueba


def eliminar_prueba(db: Session, id: int):
    prueba = db.get(Prueba, id)

    if prueba is None:
        return None

    db.delete(prueba)
    db.commit()

    return prueba
