
from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Cita(Base):
    __tablename__ = "citas" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, fecha y hora
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # requerido, máximo 200 caracteres
    motivo: Mapped[str] = mapped_column(String(300), nullable=False)
    # requerido
    #  veterinario_id: Mapped[int] = mapped_column(ForeignKey("veterinarios.id"), nullable=False)
    veterinario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # requerido
    # mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id"), nullable=False)
    mascota_id: Mapped[int] = mapped_column(Integer, nullable=False)
