"""
Router de páginas web
Contienen los endpoints que renderizan HTMLs
"""

from fastapi import APIRouter
from app.routers.web import home
from app.routers.web import mascotas
from app.routers.web import veterinario
from app.routers.web import duenyo
from app.routers.web import tratamiento
from app.routers.web import cita
from app.routers.web import inventario
 
router = APIRouter()
 
router.include_router(home.router)
router.include_router(mascotas.router)
router.include_router(veterinario.router)
router.include_router(duenyo.router)
router.include_router(tratamiento.router)
router.include_router(cita.router)
router.include_router(inventario.router)
