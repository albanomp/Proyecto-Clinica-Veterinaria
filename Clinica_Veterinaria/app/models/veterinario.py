from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

class Veterinario(Base):
    __tablename__="Veterinarios"
    id: Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre: Mapped[str]=mapped_column(String(200),nullable=False)
    colegiado: Mapped[int]=mapped_column(Integer,nullable=False)
    especialidad: Mapped[str]=mapped_column(String(200),nullable=False)
    telefono: Mapped[int]=mapped_column(Integer,nullable=False)