from fastapi import FastAPI
from app.routes.api import router as api_router
from app.database import init_db
from app.routes.web import router as web_router


app= FastAPI(title="Veterinaria",version="1.0.0")

init_db()

app.include_router(api_router)
app.include_router(web_router)


#uvicorn pruebas:app  --reload
#http://127.0.0.1:8000