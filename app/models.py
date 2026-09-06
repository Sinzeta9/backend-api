from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

    pruebas: Mapped[list[Prueba]] = relationship(
        back_populates="categoria",
    )


class Prueba(Base):
    __tablename__ = "prueba"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categoria.id"),
        nullable=True,
    )

    categoria: Mapped[Categoria | None] = relationship(
        back_populates="pruebas",
    )
