from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.duenyo import Duenyo
from app.schemas.duenyo import (
    DuenyoResponse,
    DuenyoCreate,
    DuenyoUpdate,
    DuenyoPatch
)

router = APIRouter(prefix="/api/duenyos", tags=["duenyos"])


@router.get("", response_model=list[DuenyoResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Duenyo)).scalars().all()

@router.get("/{id}", response_model=DuenyoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el dueño con id {id}"
        )
    return duenyo

@router.post("", response_model=DuenyoResponse, status_code=status.HTTP_201_CREATED)
def create(duenyo_dto: DuenyoCreate, db: Session = Depends(get_db)):

    duenyo = Duenyo(
        nombre=duenyo_dto.nombre,
        telefono=duenyo_dto.telefono,
        email=duenyo_dto.email,
        direccion=duenyo_dto.direccion
    )

    db.add(duenyo)
    db.commit()
    db.refresh(duenyo)
    return duenyo

@router.put("/{id}", response_model=DuenyoResponse)
def update_full(id: int, duenyo_dto: DuenyoUpdate, db: Session = Depends(get_db)):

    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el dueño con id {id}"
        )

    update_data = duenyo_dto.model_dump()

    for field, value in update_data.items():
        setattr(duenyo, field, value)

    db.commit()
    db.refresh(duenyo)
    return duenyo

@router.patch("/{id}", response_model=DuenyoResponse)
def update_partial(id: int, duenyo_dto: DuenyoPatch, db: Session = Depends(get_db)):

    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el dueño con id {id}"
        )

    update_data = duenyo_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(duenyo, field, value)

    db.commit()
    db.refresh(duenyo)
    return duenyo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):

    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el dueño con id {id}"
        )

    db.delete(duenyo)
    db.commit()
    return None
