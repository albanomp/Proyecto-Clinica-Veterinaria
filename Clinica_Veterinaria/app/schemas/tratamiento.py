from pydantic import BaseModel, ConfigDict
from enum import Enum


class TipoTratamiento(str, Enum):
    vacuna = "vacuna"
    medicamento = "medicamento"
    cirugia = "cirugia"
    estetico = "estetico"
    otro = "otro"

class TratamientoCreate(BaseModel):
    nombre: str
    costo: float = 0.0
    tipo: TipoTratamiento = TipoTratamiento.otro
    descripcion: str = ""
    duracion: str = "1 día"
    ingreso: bool = False


class TratamientoUpdate(BaseModel):
    nombre: str
    costo: float
    tipo: TipoTratamiento
    descripcion: str
    duracion: str
    ingreso: bool


class TratamientoPatch(BaseModel):
    nombre: str | None = None
    costo: float | None = None
    tipo: TipoTratamiento | None = None
    descripcion: str | None = None
    duracion: str | None = None
    ingreso: bool | None = None


class TratamientoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    costo: float
    tipo: str
    descripcion: str
    duracion: str
    ingreso: bool