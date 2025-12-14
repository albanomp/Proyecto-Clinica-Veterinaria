"""
Ruta web para página de inicio
Renderiza un HTML
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates import templates

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request}
    )