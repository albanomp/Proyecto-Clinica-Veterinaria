from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tratamiento import Tratamiento
from app.database import get_db

templates = Jinja2Templates(directory="Clinica_veterinaria/app/templates")

router = APIRouter(prefix="/tratamientos", tags=["web"])

@router.get("/", response_class=HTMLResponse)
def lista_tratamientos(request: Request, db: Session = Depends(get_db)):
    tratamientos = db.execute(select(Tratamiento)).scalars().all()

    return templates.TemplateResponse(
        "tratamientos/list.html",
        {"request": request, "tratamientos": tratamientos}
    )

@router.get("/{tratamiento_id}", response_class=HTMLResponse)
def detalle_tratamiento(tratamiento_id: int, request: Request, db: Session = Depends(get_db)):
    tratamiento = db.execute(
        select(Tratamiento).where(Tratamiento.id == tratamiento_id)
    ).scalar_one_or_none()

    if tratamiento is None:
        raise HTTPException(status_code=404, detail="404 - Tratamiento no encontrado")

    return templates.TemplateResponse(
        "tratamientos/detail.html",
        {"request": request, "tratamiento": tratamiento}
    )
