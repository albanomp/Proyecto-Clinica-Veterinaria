from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


class Mascota(Base):
    __tablename__="Mascotas"
    id: Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre: Mapped[str]=mapped_column(String(200),nullable=False)
    especie: Mapped[str]=mapped_column(String(200),nullable=False)
    raza: Mapped[str]=mapped_column(String(200),nullable=False)
    fecha_nacimiento: Mapped[str]=mapped_column(String(200),nullable=False)
    chip:Mapped[bool|None] = mapped_column(Boolean, nullable=True)