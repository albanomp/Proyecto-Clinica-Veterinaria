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


class Dueno(Base):
    __tablename__ = "duenos" 
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str | None] = mapped_column(Integer, nullable=True)
    direccion: Mapped[str | None] = mapped_column(Boolean, nullable=True)
    

class DuenoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    
    
class DuenoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    

class DuenoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    

class DuenoPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    telefono: str
    email: str | None
    direccion: str | None
    
Base.metadata.create_all(engine)

def init_db():
    """
    Inicializa la base de datos con algunos dueños por defecto si está vacía.
    """
    db = SessionLocal()
    try:
        existing = db.execute(select(Dueno)).scalars().all()
        if existing:
            return

        default_duenos = [
            Dueno(nombre="Paola", telefono="612345678", email="paola80@gmail.com", direccion= "Calle Los Olivos 23"),
            Dueno(nombre="Carlos", telefono="678912345",email="carlos79@gmail.com" ,direccion= "Av. Gran Canaria 45"),
            Dueno(nombre="Lucía", telefono="698745632",email="lucia98@gmail.com" ,direccion= "Calle San Sebastián 12"),
            Dueno(nombre="Kevin", telefono="657893221",email="kevin91@gmail.com" ,direccion="Calle Jerusalén 66"),
            Dueno(nombre="Samira", telefono="676356579",email="samira_93@gmail.com" ,direccion="Av.del Cabildo 57"),
            Dueno(nombre="Roberto", telefono="722345987",email="roberto@gmail.com" ,direccion="Calle Hebanista 34"),
            Dueno(nombre="Antonia", telefono="928576576",email="" ,direccion="")
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
    
    
    
