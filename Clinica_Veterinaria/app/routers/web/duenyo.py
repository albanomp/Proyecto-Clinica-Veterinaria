from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.duenyo import Duenyo

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/duenyos", tags=["web"])


@router.get("", response_class=HTMLResponse)
def list_duenyos(request: Request, db: Session = Depends(get_db)):
    duenyos = db.execute(select(Duenyo)).scalars().all()

    return templates.TemplateResponse(
        "duenyos/list.html",
        {"request": request, "duenyos": duenyos}
    )
