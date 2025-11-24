from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Mascota
from app.database import get_db


templates= Jinja2Templates(directory="Canciones/app/templates")

router= APIRouter(prefix="/mascotas",tags=["web"])

@router.get("/", response_class=HTMLResponse)
def lista(request: Request, db:Session = Depends(get_db)):
   mascotas = db.execute(select(Mascota)).scalars().all()
   return templates.TemplateResponse(
       "mascotas/list.html",
       {"request":request, "mascotas":mascotas}
       
   )