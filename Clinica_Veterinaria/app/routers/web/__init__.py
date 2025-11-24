"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from fastapi import APIRouter
from app.routes.web import home
from app.routes.web import mascotas


router = APIRouter()

router.include_router(home.router)
router.include_router(mascotas.router)
