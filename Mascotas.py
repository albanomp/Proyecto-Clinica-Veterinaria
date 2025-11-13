from fastapi import Depends, FastAPI, Query, Header, HTTPException, status
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import Integer, String, Float, Boolean, create_engine, select

engine= create_engine(
    "sqlite:///Mascotas.db", 
    echo=True, 
    connect_args={"check_same_thread":False}
)

Sessionlocal= sessionmaker(
    bind=engine,
    autocommit = False,
    autoflush= True,
    expire_on_commit= False
)

class Base(DeclarativeBase):
 pass

class Mascota(Base):
    __tablename__="Mascotas"
    id: Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre: Mapped[str]=mapped_column(String(200),nullable=False)
    especie: Mapped[str]=mapped_column(String(200),nullable=False)
    raza: Mapped[str]=mapped_column(String(200),nullable=False)
    fecha_nacimiento: Mapped[str]=mapped_column(String(200),nullable=False)
    chip:Mapped[bool|None] = mapped_column(Boolean, nullable=True)
    
class RespuestaMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None

class CrearMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None
    
class ActualizarMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    especie: str
    raza: str
    fecha_nacimiento: str
    chip: bool | None

class ParcheMascota(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str | None = None
    especie: str | None = None
    raza: str | None = None
    fecha_nacimiento: str | None = None
    chip: bool | None = None 


Base.metadata.create_all(engine)

def init_db():
    db=Sessionlocal()
    try:
        mascota_registrada=db.execute(select(Mascota)).scalars().all()
        if mascota_registrada:
            return
        mascota_encontrada=[
            Mascota(nombre="Alejandro",especie="tortuga",raza= "estrellada", fecha_nacimiento= "11-09-2001", chip=True),
            Mascota(nombre="Balboa",especie="Perro",raza= "Pastor alemán", fecha_nacimiento= "28-11-2018", chip=False),
            Mascota(nombre="Carlos",especie="Ave",raza= "Grajilla", fecha_nacimiento= "16-03-2021", chip=True),
            Mascota(nombre="Deme",especie="Reptil",raza= "Serpiente Boa", fecha_nacimiento= "7-01-2016", chip=False),
            Mascota(nombre="Elena",especie="Gato",raza= "negro", fecha_nacimiento= "17-07-2023", chip=True),
            Mascota(nombre="Fabricio",especie="Ave",raza= "Pájaro Carpintero", fecha_nacimiento= "19-09-2024", chip=True),
            Mascota(nombre="Gabriel",especie="Reptil",raza= "Dragón de Komodo", fecha_nacimiento= "30-08-2015", chip=False),
        ]
        db.add_all(mascota_encontrada)
        db.commit()
    finally:
        db.close()

init_db()

def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()

app= FastAPI()

@app.get("/")
def home():
    return {"mensaje":"Bienvenido a la clínica veterinaria Joralmar"}


@app.get("/api/mascotas",response_model=list[RespuestaMascota])
def todas_las_mascotas(db:Session=Depends(get_db)):
    return db.execute(select(Mascota)).scalars().all()


@app.get("/api/encontrar_mascota/{id}",response_model=RespuestaMascota)
def una_mascota(id: int, db:Session=Depends(get_db)):
 mascota= db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
 if not mascota:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= "404- Mascota no encontrada")
 return mascota

@app.post("/api/crear_mascota", response_model=CrearMascota, status_code= status.HTTP_201_CREATED)
def create(mascota_dto: CrearMascota,db:Session=Depends(get_db)):
    if not mascota_dto.nombre.strip():
        raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
    if not mascota_dto.especie.strip():
        raise HTTPException(status_code=400, detail= "La especie no puede estar vacío")
    if not mascota_dto.raza.strip():
        raise HTTPException(status_code=400, detail= "La raza no puede estar vacío")
    if not mascota_dto.fecha_nacimiento.strip():
        raise HTTPException(status_code=400, detail= "La fecha no puede estar vacía")
    mascota_dto=Mascota(
        nombre= mascota_dto.nombre.strip(), especie= mascota_dto.especie.strip(), 
        raza= mascota_dto.raza.strip(),fecha_nacimiento= mascota_dto.fecha_nacimiento.strip(), 
        chip= mascota_dto.chip
        )
    db.add(mascota_dto)
    db.commit()
    db.refresh(mascota_dto)
    return mascota_dto

@app.delete("/api/eliminar_mascota/{id}",response_model=RespuestaMascota)
def eliminar_mascota(id: int, db:Session=Depends(get_db)):
    mascota=db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
    if not mascota:
     raise HTTPException(status_code=404, detail= "404- Mascota registrada no encontrada")
    db.delete(mascota)
    db.commit()
    return mascota



#uvicorn Mascotas:app  --reload