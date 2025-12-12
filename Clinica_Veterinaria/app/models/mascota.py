from __future__ import annotations
from typing import TYPE_CHECKING
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Boolean

if TYPE_CHECKING:
    from .duenyo import Duenyo

class Mascota(Base):
    __tablename__="Mascotas"
    id: Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre: Mapped[str]=mapped_column(String(200),nullable=False)
    especie: Mapped[str]=mapped_column(String(200),nullable=False)
    raza: Mapped[str]=mapped_column(String(200),nullable=False)
    fecha_nacimiento: Mapped[str]=mapped_column(String(200),nullable=False)
    chip:Mapped[bool|None] = mapped_column(Boolean, nullable=True)
    duenyo_id: Mapped[int] = mapped_column(ForeignKey("duenyos.id"), nullable=False)
    duenyo: Mapped["Duenyo"] = relationship(back_populates="mascotas")