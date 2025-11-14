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
    """
    Inicializa la base de datos con algunos dueños por defecto si está vacía.
    """
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

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

"""
VIDEO
- id: int
- title: string (obligatorio)
- channel: string (obligatorio)
- views: entero (opcional)
- has_subtitles: booleano (opcional)
"""

# CONFIGURACIÓN DE BASE DE DATOS
# motor de conexión
engine = create_engine(
    "sqlite:///09_sqlalchemy/videos.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


# MODELO DE BASE DE DATOS (SQLALCHEMY)
# clase base
class Base(DeclarativeBase):
    pass

# modelo de tabla videos
class Video(Base):
    __tablename__ = "videos"
    
    # id, clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # obligatorio, 200 caracteres como máximo
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # obligatorio, 200 caracteres como máximo
    channel: Mapped[str] = mapped_column(String(200), nullable=False)
    # optional
    views: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # optional
    has_subtitles: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


# MODELOS PYDANTIC (SCHEMAS)
class VideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    channel: str
    views: int | None
    has_subtitles: bool | None

class VideoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    channel: str
    views: int | None = None
    has_subtitles: bool | None = None

class VideoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    channel: str
    views: int | None
    has_subtitles: bool | None

class VideoPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    channel: str | None = None
    views: int | None = None
    has_subtitles: bool | None = None


# INICIALIZACIÓN DE BASE DE DATOS
# crear las tablas de la base de datos
Base.metadata.create_all(engine)

# poblar tablas
def init_db():
    db = SessionLocal()
    try:
        existing_videos = db.execute(select(Video)).scalars().all()
        
        if existing_videos:
            return
        
        default_videos = [
            Video(title="Grajillas cantanto", channel="La Grajilla", views=9999999, has_subtitles=True),
            Video(title="Curso de FastAPI", channel="Gente muy pro", views=5000, has_subtitles=False),
            Video(title="Cómo instalar Linux", channel="Linux el mejor", views=25000, has_subtitles=True),
            Video(title="Música ASMR para dormir", channel="ASMR para todos", views=400, has_subtitles=False),
            Video(title="Cómo atraer aves a tu jardín", channel="Avibérico", views=8080, has_subtitles=True)
        ]
        
        db.add_all(default_videos)
        db.commit()
    finally:
        db.close()

init_db()

# DEPENDENCIA DE FASTPI
# método para dar sesión de base de datos al endpoint
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