from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from app.database import get_db
from app.models.tratamiento import Tratamiento
from app.models.inventario import Inventario
from app.models.inventario_tratamiento import tratamiento_inventario
from app.schemas.inventario_tratamiento import AsignarInventarioDTO
 
router = APIRouter(prefix="/api/tratamientos", tags=["inventario_tratamientos"])
 
@router.post("/{tratamiento_id}/inventario", status_code=status.HTTP_201_CREATED)
def asignar_inventario_a_tratamiento(
    tratamiento_id: int,
    data: AsignarInventarioDTO,
    db: Session = Depends(get_db)
):
   
# Esta parte es para comprobar que existe el tto
   tratamiento = db.execute(
       select(Tratamiento).where(Tratamiento.id == tratamiento_id)
       ).scalar_one_or_none()
   if not tratamiento:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Tratamiento no encontrado"
       )
   
# Aquí comprobamos que existe el inventario
   inventario = db.execute(
        select(Inventario).where(Inventario.id == data.inventario_id)
    ).scalar_one_or_none()
   if not inventario:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=f"Producto de inventario no encontrado"
       )
   
    # Comprobamos si hay stock suficiente
   if inventario.cantidad < data.cantidad_usada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay suficiente stock en inventario"
        )
   
    # Insertar en la tabla intermedia
   db.execute(
        insert(tratamiento_inventario).values(
            tratamiento_id=tratamiento_id,
            inventario_id=data.inventario_id,
            cantidad_usada=data.cantidad_usada
        )
    )
 
    # Restar stock
   inventario.cantidad -= data.cantidad_usada
 
   db.commit()
 
   return {
        "mensaje": "Inventario asignado al tratamiento correctamente"
    }