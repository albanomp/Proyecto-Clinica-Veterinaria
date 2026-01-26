from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base
 
tratamiento_inventario = Table(
    "tratamiento_inventario",
    Base.metadata,
    Column("tratamiento_id", ForeignKey("tratamientos.id"), primary_key=True),
    Column("inventario_id", ForeignKey("inventario.id"), primary_key=True),
    Column("cantidad_usada", Integer, nullable=False, default=1)
)