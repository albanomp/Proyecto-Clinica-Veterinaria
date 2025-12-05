from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.tratamiento import Tratamiento

templates = Jinja2Templates(directory="Clinica_veterinaria/app/templates")

router = APIRouter(prefix="/tratamientos", tags=["web"])


@router.get("", response_class=HTMLResponse)
def list_tratamientos(request: Request, db: Session = Depends(get_db)):
    tratamientos = db.execute(select(Tratamiento)).scalars().all()

    return templates.TemplateResponse(
        "tratamientos/list.html",
        {"request": request, "tratamientos": tratamientos}
    )
