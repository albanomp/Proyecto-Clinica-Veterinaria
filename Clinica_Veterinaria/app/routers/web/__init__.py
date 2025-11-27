"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from fastapi import APIRouter
from app.routes.web import home
from app.routes.web import mascotas
from app.routes.web import veterinario
from app.routes.web import duenyo
from app.routes.web import tratamiento


router = APIRouter()

router.include_router(home.router)
router.include_router(mascotas.router)
router.include_router(veterinario.router)
router.include_router(duenyo.router)
router.include_router(tratamiento.router)
