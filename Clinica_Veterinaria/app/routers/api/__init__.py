from fastapi import APIRouter
from app.routers.api import duenyos
from app.routers.api import mascotas
from app.routers.api import tratamientos
from app.routers.api import veterinarios

router = APIRouter()

router.include_router(mascotas.router)
router.include_router(duenyos.router)
router.include_router(tratamientos.router)
router.include_router(veterinarios.router)
