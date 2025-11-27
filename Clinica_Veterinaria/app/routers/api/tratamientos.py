from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tratamiento import Tratamiento
from app.schemas.tratamiento import (
    TratamientoResponse,
    TratamientoCreate,
    TratamientoUpdate,
    TratamientoPatch
)

router = APIRouter(prefix="/api/tratamientos", tags=["tratamientos"])

@router.get("", response_model=list[TratamientoResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Tratamiento)).scalars().all()

@router.get("/{id}", response_model=TratamientoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    tratamiento = db.execute(
        select(Tratamiento).where(Tratamiento.id == id)
    ).scalar_one_or_none()

    if not tratamiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe tratamiento con id {id}"
        )
    return tratamiento


@router.post("", response_model=TratamientoResponse, status_code=status.HTTP_201_CREATED)
def create(tr_dto: TratamientoCreate, db: Session = Depends(get_db)):

    tratamiento = Tratamiento(
        nombre=tr_dto.nombre,
        costo=tr_dto.costo,
        tipo=tr_dto.tipo,
        descripcion=tr_dto.descripcion,
        duracion=tr_dto.duracion,
        ingreso=tr_dto.ingreso
    )

    db.add(tratamiento)
    db.commit()
    db.refresh(tratamiento)
    return tratamiento


@router.put("/{id}", response_model=TratamientoResponse)
def update_full(id: int, tr_dto: TratamientoUpdate, db: Session = Depends(get_db)):

    tratamiento = db.execute(
        select(Tratamiento).where(Tratamiento.id == id)
    ).scalar_one_or_none()

    if not tratamiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe tratamiento con id {id}"
        )

    update_data = tr_dto.model_dump()

    for field, value in update_data.items():
        setattr(tratamiento, field, value)

    db.commit()
    db.refresh(tratamiento)
    return tratamiento


@router.patch("/{id}", response_model=TratamientoResponse)
def update_partial(id: int, tr_dto: TratamientoPatch, db: Session = Depends(get_db)):

    tratamiento = db.execute(
        select(Tratamiento).where(Tratamiento.id == id)
    ).scalar_one_or_none()

    if not tratamiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe tratamiento con id {id}"
        )

    update_data = tr_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(tratamiento, field, value)

    db.commit()
    db.refresh(tratamiento)
    return tratamiento


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):

    tratamiento = db.execute(
        select(Tratamiento).where(Tratamiento.id == id)
    ).scalar_one_or_none()

    if not tratamiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe tratamiento con id {id}"
        )

    db.delete(tratamiento)
    db.commit()
    return None
