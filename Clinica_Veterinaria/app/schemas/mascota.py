

from pydantic import BaseModel, ConfigDict


class RespuestaMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None

class CrearMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None
    
class ActualizarMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None

class ParcheMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str | None = None
    especie: str | None = None
    raza: str | None = None
    fecha_nacimiento: str | None = None
    chip: bool | None = None