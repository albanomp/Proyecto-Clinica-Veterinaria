from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
 
 
class InventarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    id: int
    nombre: str
    tipo: str
    cantidad: int
    precio: float | None
    fecha_caducidad: datetime
    activo: bool
 
 
class InventarioCrear(BaseModel):
    nombre: str
    tipo: str
    cantidad: int
    precio: float | None
    fecha_caducidad: datetime
    activo: bool
 
    @field_validator("nombre", "tipo")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede quedar vacío")
        return v.strip()
 
 
class InventarioActualizar(BaseModel):
    nombre: str
    tipo: str
    cantidad: int
    precio: float | None
    fecha_caducidad: datetime
    activo: bool
 
    @field_validator("nombre", "tipo")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede quedar vacío")
        return v.strip()
 
 
class ParcheInventario(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    cantidad: int | None = None
    precio: float | None = None
    fecha_caducidad: datetime | None = None
    activo: bool | None = None
 
    @field_validator("nombre", "tipo")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Este campo no puede quedar vacío")
        return v.strip() if v else v