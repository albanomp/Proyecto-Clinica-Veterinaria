
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CitaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int
    
class CitaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int

class CitaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int

class CitaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime | None = None
    motivo: str | None = None
    veterinario_id: int | None = None
    mascota_id: int | None = None

