



from pydantic import BaseModel, ConfigDict, field_validator


class RespuestaMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None
    @field_validator("nombre","especie","raza","fecha_nacimiento")
    @classmethod
    def validate_not_empty(RespuestaMascota, m:str)->str:
        if not m or not m.strip():
            raise ValueError("Este campo no puede estar vacio")
        return m.strip()

class CrearMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None
    @field_validator("nombre","especie","raza","fecha_nacimiento")
    @classmethod
    def validate_not_empty(RespuestaMascota, m:str)->str:
        if not m or not m.strip():
            raise ValueError("Este campo no puede estar vacio")
        return m.strip()
    
class ActualizarMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None
    @field_validator("nombre","especie","raza","fecha_nacimiento")
    @classmethod
    def validate_not_empty(RespuestaMascota, m:str)->str:
        if not m or not m.strip():
            raise ValueError("Este campo no puede estar vacio")
        return m.strip()

class ParcheMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str | None = None
    especie: str | None = None
    raza: str | None = None
    fecha_nacimiento: str | None = None
    chip: bool | None = None
