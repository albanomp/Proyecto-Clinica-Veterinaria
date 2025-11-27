from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Veterinario
from app.database import get_db


templates= Jinja2Templates(directory="Canciones/app/templates")

router= APIRouter(prefix="/veterinarios",tags=["web"])

@router.get("/", response_class=HTMLResponse)
def lista_empleado(request: Request, db:Session = Depends(get_db)):
   veterinarios = db.execute(select(Veterinario)).scalars().all()
   return templates.TemplateResponse(
       "veterinarios/list.html",
       {"request":request, "veterinarios":veterinarios}
       
   )

@router.get("/{veterinario_id}", response_class=HTMLResponse)
def lista_mascota(veterinario_id: int, request: Request, db:Session = Depends(get_db)):
   veterinario= db.execute(select(Veterinario).where(Veterinario.id == veterinario_id)).scalar_one_or_none()
   if veterinario is None:
       raise HTTPException(status_code=404, detail= "404 - veterinario no registrado")
   return templates.TemplateResponse(
       "veterinarios/detalle.html",
       {"request":request, "veterinario":veterinario}
       
   )