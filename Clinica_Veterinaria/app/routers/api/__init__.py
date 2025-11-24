from fastapi import APIRouter

from app.routes.api import mascotas

router = APIRouter()

router.include_router(mascotas.router)
