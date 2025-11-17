from fastapi import Depends, FastAPI, Query, Header, HTTPException, status
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from sqlalchemy import Integer, String, Float, Boolean, create_engine, select

engine= create_engine(
    "sqlite:///Veterinarios.db", 
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

class Veterinario(Base):
    __tablename__="Veterinarios"
    id: Mapped[int]=mapped_column(Integer,primary_key=True, autoincrement=True)
    nombre: Mapped[str]=mapped_column(String(200),nullable=False)
    colegiado: Mapped[int]=mapped_column(Integer,nullable=False)
    especialidad: Mapped[str]=mapped_column(String(200),nullable=False)
    telefono: Mapped[int]=mapped_column(Integer,nullable=False)
    
class RespuestaVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int

class CrearVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int
    
class ActualizarVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str
    colegiado: int
    especialidad: str
    telefono: int

class ParcheVeterinario(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    nombre: str | None = None
    colegiado: int | None = None
    especialidad: str | None = None
    telefono: int | None = None


Base.metadata.create_all(engine)

def init_db():
    db=Sessionlocal()
    try:
        veterinario_empleado=db.execute(select(Veterinario)).scalars().all()
        if veterinario_empleado:
            return
        veterinario_empleados=[
            Veterinario(nombre="Albano",colegiado=12345,especialidad= "Reptiles", telefono= 666890121),
            Veterinario(nombre="Borja",colegiado=11346,especialidad= "Mamiferos", telefono= 654761015),
            Veterinario(nombre="Carlota",colegiado=15925,especialidad= "Oviparos", telefono= 672315692),
            Veterinario(nombre="Estefania",colegiado=21674,especialidad= "Inyecciones", telefono= 612362891),
        ]
        db.add_all(veterinario_empleados)
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


@app.get("/api/veterinarios",response_model=list[RespuestaVeterinario])
def todos_las_veterinarios(db:Session=Depends(get_db)):
    return db.execute(select(Veterinario)).scalars().all()


@app.get("/api/encontrar_veterinario/{id}",response_model=RespuestaVeterinario)
def un_veterinario(id: int, db:Session=Depends(get_db)):
 veterinario= db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
 if not veterinario:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= "404- Veterinario no encontrada")
 return veterinario

@app.post("/api/crear_veterinario", response_model=CrearVeterinario, status_code= status.HTTP_201_CREATED)
def create(veterinario_dto: CrearVeterinario,db:Session=Depends(get_db)):
    if not veterinario_dto.nombre.strip():
        raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
    if not veterinario_dto.especie.strip():
        raise HTTPException(status_code=400, detail= "El colegiado no puede estar vacío")
    if not veterinario_dto.raza.strip():
        raise HTTPException(status_code=400, detail= "La especialidad no puede estar vacío")
    if not veterinario_dto.fecha_nacimiento.strip():
        raise HTTPException(status_code=400, detail= "El telefono no puede estar vacío")
    veterinario_dto=Veterinario(
        nombre= veterinario_dto.nombre.strip(), colegiado= veterinario_dto.colegiado.strip(), 
        especialidad= veterinario_dto.especialidad.strip(),telefono= veterinario_dto.telefono.strip()
        )
    db.add(veterinario_dto)
    db.commit()
    db.refresh(veterinario_dto)
    return veterinario_dto

@app.put("/api/actualizar_veterinario/{id}", response_model=ActualizarVeterinario)
def update(id:int, veterinario_dto: ActualizarVeterinario,db:Session=Depends(get_db)):
    veterinario_dto = db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    if not veterinario_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado el veterinario con id {id}"
        )
    if not veterinario_dto.nombre.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre no puede estar vacío."
        )       
        
    if not veterinario_dto.especie.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El colegiado no puede estar vacío."
        )    
    
    if not veterinario_dto.raza.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La especialidad no puede estar vacía."
        )
    if not veterinario_dto.fecha_nacimiento.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El telefono no puede estar vacío."
        )        

    veterinario_dto.nombre= veterinario_dto.nombre.strip()
    veterinario_dto.colegiado= veterinario_dto.colegiado.strip()
    veterinario_dto.especialidad= veterinario_dto.especialidad.strip()
    veterinario_dto.telefono= veterinario_dto.telefono.strip()
    
    db.commit()
    db.refresh(veterinario_dto)
    return veterinario_dto



@app.patch("/api/parchear_veterinario", response_model=ParcheVeterinario)
def parche(id:int, veterinario_dto: ParcheVeterinario,db:Session=Depends(get_db)):
    veterinario= db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    
    if not veterinario_dto:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= f"404- Veterinario con {id} no encontrado")
 
    if veterinario_dto.nombre is not None:
        if not veterinario_dto.nombre.strip():
         raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
        veterinario.nombre = veterinario_dto.nombre.strip()
    
    if veterinario_dto.colegiado is not None:
        if not veterinario_dto.colegiado.strip():
         raise HTTPException(status_code=400, detail= "El colegiado no puede estar vacío")
        veterinario.colegiado = veterinario_dto.colegiado.strip()
    
    
    if veterinario_dto.especialidad is not None:
        if not veterinario_dto.raza.strip():
         raise HTTPException(status_code=400, detail= "La especialidad no puede estar vacía")
        veterinario.especialidad = veterinario_dto.especialidad.strip()
    
    if veterinario_dto.telefono is not None:
        if not veterinario_dto.telefono.strip():
         raise HTTPException(status_code=400, detail= "El telefono no puede estar vacío")
        veterinario.telefono = veterinario_dto.telefono.strip()
    
    
    db.commit()
    db.refresh(veterinario)
    return veterinario


@app.delete("/api/eliminar_veterinario/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_veterinario(id: int, db:Session=Depends(get_db)):
    veterinario=db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    if not veterinario:
     raise HTTPException(status_code=404, detail= "404- Veterinario ya no trabaja aqui")
    db.delete(veterinario)
    db.commit()
    return None
#uvicorn Veterinario:app  --reload
#http://127.0.0.1:8000