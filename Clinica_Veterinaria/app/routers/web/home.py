"""
Ruta web para página de inicio
Renderiza un HTML
"""

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# configurar jinja2
templates = Jinja2Templates(directory="Clinica_Veterinaria/app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )