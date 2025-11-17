from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session


engine = create_engine(
    "sqlite:///09_sqlalchemy/clinica.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


class Duenyo(Base):
    __tablename__ = "duenyos" 
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(Integer, nullable=True)
    direccion: Mapped[str | None] = mapped_column(Boolean, nullable=True)
    

class DuenyoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    
    
class DuenyoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None = None
    direccion: str | None = None
    

class DuenyoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    

class DuenyoPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None = None
    direccion: str | None = None
    
Base.metadata.create_all(engine)

def init_db():
    
    db = SessionLocal()
    try:
        existing = db.execute(select(Duenyo)).scalars().all()
        if existing:
            return

        default_duenos = [
            Duenyo(nombre="Paola", telefono="612345678", email="paola80@gmail.com", direccion= "Calle Los Olivos 23"),
            Duenyo(nombre="Carlos", telefono="678912345",email="carlos79@gmail.com" ,direccion= "Av. Gran Canaria 45"),
            Duenyo(nombre="Lucía", telefono="698745632",email="lucia98@gmail.com" ,direccion= "Calle San Sebastián 12"),
            Duenyo(nombre="Kevin", telefono="657893221",email="kevin91@gmail.com" ,direccion="Calle Jerusalén 66"),
            Duenyo(nombre="Samira", telefono="676356579",email="samira_93@gmail.com" ,direccion="Av.del Cabildo 57"),
            Duenyo(nombre="Roberto", telefono="722345987",email="roberto@gmail.com" ,direccion="Calle Hebanista 34"),
            Duenyo(nombre="Antonia", telefono="928576576",email="" ,direccion="")
        ]
        db.add_all(default_duenos)
        db.commit()
    finally:
        db.close()

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app = FastAPI(title="Clínica Veterinaria", version="1.0.0")



Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="App clinica veterinaria", version="1.1.4")

@app.get("/")
def home():
    return {"mensaje": "Gracias por confiar wn nuestra aplicacion de clinicas veterinarias <3 "}

@app.get("/api/Clinica", response_model=list[DuenyoResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Duenyo)).scalars().all()

@app.get("/api/clinica/{id}", response_model=DuenyoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):   
    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()
    
    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    return duenyo

@app.post("/api/duenos", response_model=DuenyoResponse, status_code=status.HTTP_201_CREATED)
def create_dueno(dueno_dto: DuenyoCreate, db: Session = Depends(get_db)):
    if not dueno_dto.nombre.strip():
        raise HTTPException(status_code=400, detail="El nombre del dueño no puede estar vacío")
    if not dueno_dto.telefono.strip():
        raise HTTPException(status_code=400, detail="El teléfono del dueño no puede estar vacío")

    nuevo_duenyo = Duenyo(
        nombre=dueno_dto.nombre.strip(),
        telefono=dueno_dto.telefono.strip(),
        direccion=dueno_dto.direccion
    )
    db.add(nuevo_duenyo)
    db.commit()
    db.refresh(nuevo_duenyo)
    return 

@app.patch("/api/duenyo/{id}", response_model=DuenyoResponse)
def update_partial(id: int, duenyo_dto: DuenyoPatch, db: Session = Depends(get_db)):
    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el dueño con id {id}"
        )

    if duenyo_dto.nombre is not None:
        if not duenyo_dto.nombre.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre no puede estar vacío"
            )
        duenyo.nombre = duenyo_dto.nombre.strip()

    if duenyo_dto.telefono is not None:
        if not duenyo_dto.telefono.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El teléfono no puede estar vacío"
            )
        duenyo.telefono = duenyo_dto.telefono.strip()

    if duenyo_dto.direccion is not None:
        duenyo.direccion = duenyo_dto.direccion

    db.commit()
    db.refresh(duenyo)

    return duenyo

@app.delete("/api/duenyo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    duenyo = db.execute(
        select(Duenyo).where(Duenyo.id == id)
    ).scalar_one_or_none()

    if not duenyo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el dueño con id {id}"
        )

    db.delete(duenyo)
    db.commit()
    return None