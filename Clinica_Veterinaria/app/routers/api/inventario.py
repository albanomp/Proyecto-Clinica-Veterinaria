from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
 
from app.database import get_db
from app.models.inventario import Inventario
from app.schemas.inventario import (
    InventarioRespuesta,
    InventarioCrear,
    InventarioActualizar,
    ParcheInventario
)
 
router = APIRouter(prefix="/api/inventario", tags=["inventario"])
 
 
@router.get("", response_model=list[InventarioRespuesta])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Inventario)).scalars().all()
 
 
@router.get("/{id}", response_model=InventarioRespuesta)
def find_by_id(id: int, db: Session = Depends(get_db)):
    inventario = db.execute(
        select(Inventario).where(Inventario.id == id)
    ).scalar_one_or_none()
 
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el producto con id {id}"
        )
 
    return inventario
 
 
@router.post("", response_model=InventarioRespuesta, status_code=status.HTTP_201_CREATED)
def create(inventario_dto: InventarioCrear, db: Session = Depends(get_db)):
 
    inventario = Inventario(
        nombre=inventario_dto.nombre,
        tipo=inventario_dto.tipo,
        cantidad=inventario_dto.cantidad,
        precio=inventario_dto.precio,
        fecha_caducidad=inventario_dto.fecha_caducidad,
        activo=inventario_dto.activo
    )
 
    db.add(inventario)
    db.commit()
    db.refresh(inventario)
    return inventario
 
 
@router.put("/{id}", response_model=InventarioRespuesta)
def update_full(id: int, inventario_dto: InventarioActualizar, db: Session = Depends(get_db)):
 
    inventario = db.execute(
        select(Inventario).where(Inventario.id == id)
    ).scalar_one_or_none()
 
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado en el inventario"
        )
 
    update_data = inventario_dto.model_dump()
 
    for field, value in update_data.items():
        setattr(inventario, field, value)
 
    db.commit()
    db.refresh(inventario)
    return inventario
 
 
@router.patch("/{id}", response_model=InventarioRespuesta)
def update_partial(id: int, inventario_dto: ParcheInventario, db: Session = Depends(get_db)):
 
    inventario = db.execute(
        select(Inventario).where(Inventario.id == id)
    ).scalar_one_or_none()
 
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el producto con id {id}"
        )
 
    update_data = inventario_dto.model_dump(exclude_unset=True)
 
    for field, value in update_data.items():
        setattr(inventario, field, value)
 
    db.commit()
    db.refresh(inventario)
    return inventario
 
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
 
    inventario = db.execute(
        select(Inventario).where(Inventario.id == id)
    ).scalar_one_or_none()
 
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el producto con id {id}"
        )
 
    db.delete(inventario)
    db.commit()
    return None
 