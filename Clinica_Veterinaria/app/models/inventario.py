from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime, Boolean
from app.models.inventario_tratamiento import tratamiento_inventario
 
if TYPE_CHECKING:
    from .tratamiento import Tratamiento
 
class Inventario(Base):
    __tablename__ = "inventario"
 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(300), nullable=False)
    tipo: Mapped[str] = mapped_column(String(200), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[float | None] = mapped_column(Float)
    fecha_caducidad: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
 
    tratamientos: Mapped[list["Tratamiento"]] = relationship(
        secondary=tratamiento_inventario,
        back_populates="inventarios"
    )