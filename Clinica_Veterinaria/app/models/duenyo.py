from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .mascota import Mascota

class Duenyo(Base):
    __tablename__ = "duenyos" 
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    direccion: Mapped[str | None] = mapped_column(String, nullable=True)
    mascotas: Mapped[List["Mascota"]] = relationship(
        back_populates="duenyo",
    )