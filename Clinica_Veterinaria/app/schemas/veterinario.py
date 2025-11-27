from pydantic import BaseModel, ConfigDict, field_validator

class RespuestaVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int
    @field_validator("nombre","especialidad")
    @classmethod
    def validate_not_empty(RespuestaVeterinario, v:str)->str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacio")
        return v.strip()



class CrearVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int
    @field_validator("nombre","especialidad")
    @classmethod
    def validate_not_empty(RespuestaVeterinario, v:str)->str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacio")
        return v.strip()
    
class ActualizarVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int
    @field_validator("nombre","especialidad")
    @classmethod
    def validate_not_empty(RespuestaVeterinario, v:str)->str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacio")
        return v.strip()
    

class ParcheVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str | None = None
    colegiado: int | None = None
    especialidad: str | None = None
    telefono: int | None = None