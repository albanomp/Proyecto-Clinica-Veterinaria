from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .mascota import Mascota

class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    duracion: Mapped[str] = mapped_column(String(100), nullable=False)
    ingreso: Mapped[bool] = mapped_column(Boolean, default=False)
    mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id", ondelete="Cascade"), nullable=False)
    mascota: Mapped["Mascota"] = relationship(back_populates="tratamientos")
    
    