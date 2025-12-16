
from __future__ import annotations
from typing import List, TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

if TYPE_CHECKING:
    from .cita import Cita

class Veterinario(Base):
    __tablename__ = "veterinarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    colegiado: Mapped[int] = mapped_column(Integer, nullable=False)
    especialidad: Mapped[str] = mapped_column(String(200), nullable=False)
    telefono: Mapped[int] = mapped_column(Integer, nullable=False)
    citas: Mapped[List["Cita"]] = relationship(
        back_populates="veterinario")