from pydantic import BaseModel, ConfigDict

class DuenyoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    
    
class DuenyoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None = None
    direccion: str | None = None
    

class DuenyoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    

class DuenyoPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None = None
    direccion: str | None = None
    