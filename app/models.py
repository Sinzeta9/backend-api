from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.base import Base


class Prueba(Base):
    __tablename__ = "prueba"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))

