
from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .veterinario import Veterinario
    from .mascota import Mascota

class Cita(Base):
    __tablename__ = "citas" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, fecha y hora
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # requerido, máximo 200 caracteres
    motivo: Mapped[str] = mapped_column(String(300), nullable=False)
    # requerido
    veterinario_id: Mapped[int] = mapped_column(ForeignKey("veterinarios.id"), nullable=False)
    veterinario: Mapped["Veterinario"] = relationship(back_populates="citas")
    #veterinario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # requerido
    mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id", ondelete="Cascade"), nullable=False)
    mascota: Mapped["Mascota"] = relationship(back_populates="citas")
