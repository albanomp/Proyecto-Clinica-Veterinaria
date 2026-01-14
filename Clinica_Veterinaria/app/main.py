from fastapi import FastAPI
from app.routers.api import router as api_router
from app.database import init_db
from app.routers.web import router as web_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app= FastAPI(title="Veterinaria",version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=BASE_DIR/"statics(imagenes)"), name="static")

init_db()

app.include_router(api_router)
app.include_router(web_router)


#uvicorn pruebas:app  --reload
#http://127.0.0.1:8000