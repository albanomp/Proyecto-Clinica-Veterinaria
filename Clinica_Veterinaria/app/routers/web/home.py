"""
Ruta web para pagina de inicio
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates= Jinja2Templates(directory="Canciones/app/templates")

router= APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request":request}
    )