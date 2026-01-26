from pydantic import BaseModel, Field
 
class AsignarInventarioDTO(BaseModel):
    inventario_id: int
    cantidad_usada: int = Field(gt=0, description="Debe ser mayor que 0")