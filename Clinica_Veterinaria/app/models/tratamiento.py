from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    duracion: Mapped[str] = mapped_column(String(100), nullable=False)
    ingreso: Mapped[bool] = mapped_column(Boolean, default=False)