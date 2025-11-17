
# Teclea en la terminal: uvicorn 09_sqlalchemy.cita:app --reload

from datetime import date, datetime
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, func, select, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

# COFIGURACION DE BASE DE DATOS

# Crear motor de conexión a base de datos



engine = create_engine(
    "sqlite:///09_sqlalchemy/citas.db",
    echo=True,
    connect_args = {"check_same_thread" : False}
)

# Crear fabrica de sesiones de base de datos

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


class Cita(Base):
    __tablename__ = "citas" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, fecha y hora
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # requerido, máximo 200 caracteres
    motivo: Mapped[str] = mapped_column(String(300), nullable=False)
    # requerido
    #  veterinario_id: Mapped[int] = mapped_column(ForeignKey("veterinarios.id"), nullable=False)
    veterinario_id: Mapped[int] = mapped_column(Integer, nullable=False)
    # requerido
    # mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id"), nullable=False)
    mascota_id: Mapped[int] = mapped_column(Integer, nullable=False)


# MODELOS PYDANTIC (schemas)
# modelos que validan los datos que llegan y salen de la api

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
class CitaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int
    

# schema para CREAR una canción (POST)
# no incluimos id porque se genera automáticamente
class CitaCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int

# schema para ACTUALIZACIÓN COMPLETA (PUT)
# todos los campos se tienen que enviar
class CitaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime
    motivo: str
    veterinario_id: int
    mascota_id: int

# schema para ACTUALIZACIÓN PARCIAL (PATCH)
# sólo se envían los campos que quieras actualizar
class CitaPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    fecha_hora: datetime | None = None
    motivo: str | None = None
    veterinario_id: int | None = None
    mascota_id: int | None = None


# INICIALIZACIÓN BASE DE DATOS

# crear todas las tablas
Base.metadata.create_all(engine)

# método inicializar con canciones por defecto
def init_db():
    """
    Inializa la base de datos con citas por defecto si está vacía.
    Sólo crea las citas si no existen ya en la base de datos.
    """
    db = SessionLocal()
    try:
        existing_citas = db.execute(select(Cita)).scalars().all()
        
        if existing_citas:
        
            return
        
        default_citas = [
            Cita( fecha_hora=datetime(2025, 12, 14, 10, 30),motivo="Vacunación",
            veterinario_id=1, mascota_id=3),
            Cita( fecha_hora=datetime(2025, 12, 23, 11, 00),motivo="Revisión",
            veterinario_id=2, mascota_id=1),
            Cita( fecha_hora=datetime(2025, 12, 21, 9, 30),motivo="Vacunación",
            veterinario_id=2, mascota_id=4),
            Cita( fecha_hora=datetime(2025, 12, 16, 10, 30),motivo="Inicial",
            veterinario_id=2, mascota_id=2),
            Cita( fecha_hora=datetime(2025, 12, 17, 10, 30),motivo="Tratamoento",
            veterinario_id=2, mascota_id=5),
            Cita( fecha_hora=datetime(2025, 12, 19, 9, 30),motivo="Vacunación",
            veterinario_id=1, mascota_id=6),
            Cita( fecha_hora=datetime(2025, 12, 19, 12, 30),motivo="Vacunación",
            veterinario_id=1, mascota_id=8)

        ]
        
        # agregar las canciones
        db.add_all(default_citas)
        db.commit()
    finally:
        db.close()

# inicializa la base de datos con canciones por defecto
init_db()


# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()



# APLICACIÓN FASTAPI

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Citas", version="1.0.0")

# endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la app de la clínica veterinaria"}

# ENDPOINTS CRUD

# GET - obtener TODAS las citas
@app.get("/api/citas", response_model=list[CitaResponse])
def find_all(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Cita): crea consulta SELECT * FROM Cita
    # .scarlars(): extrae los objetos Cita
    # .all(): obtiene los resultados como lista
    return db.execute(select(Cita)).scalars().all()


# GET - obtener UNA canción por id
@app.get("/api/citas/{id}", response_model=CitaResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca a canción con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    cita = db.execute(
        select(Cita).where(Cita.id == id)
    ).scalar_one_or_none()
    
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    return cita


@app.get("/api/citas/fecha/{fecha}", response_model=list[CitaResponse])
def find_by_fecha(fecha: date, db: Session = Depends(get_db)):

#   Devuelve todas las citas de una fecha concreta.

    cita = db.execute(
        select(Cita).where(func.date(Cita.fecha_hora) == fecha)
    ).scalars().all()

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se han encontrado citas para la fecha {fecha}"
        )
    return cita

# POST - crear una nueva cita
@app.post("/api/citas", response_model=CitaResponse, status_code = status.HTTP_201_CREATED)
def create(cita_dto: CitaCreate, db: Session = Depends(get_db)):
    # validaciones
    if not cita_dto.fecha_hora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de la cita no puede estar vacío"
        )

    if not cita_dto.motivo.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El motivo de la cita no puede estar vacío"
        )
    
    if cita_dto.veterinario_id is None or cita_dto.veterinario_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El veterinario de la cita debe tener un identificador válido"
        )
    
    if cita_dto.mascota_id is None or cita_dto.mascota_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La mascota de la cita debe tener un identificador válido"
        )

            
    # crea objeto Cira con datos validados
    cita = Cita(
        fecha_hora=cita_dto.fecha_hora,
        motivo=cita_dto.motivo.strip(),
        veterinario_id=cita_dto.veterinario_id,
        mascota_id=cita_dto.mascota_id
    )


    
    db.add(cita) # agrega el objeto a la sesión
    db.commit() # confirma la creación en base de datos
    db.refresh(cita) # refresca el objeto para obtener el id generado
    return cita # retorna la canción creada


"""
# PUT - actualizar COMPLETAMENTE una canción
@app.put("/api/songs/{id}", response_model=SongResponse)
def update_full(id: int, song_dto: SongUpdate, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # validaciones (igual que en POST)
    if not song_dto.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
    
    if not song_dto.artist.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
    
    if song_dto.duration_seconds is not None and song_dto.duration_seconds < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración debe ser un número positivo"
        )
    
    song.title = song_dto.title.strip()
    song.artist = song_dto.artist.strip()
    song.duration_seconds = song_dto.duration_seconds
    song.explicit = song_dto.explicit
    
    db.commit() # confirma los cambios
    db.refresh(song) # refresca el objeto de la base de datos
    return song # retorna la canción actualizada

# PATCH - actualizar PARCIALMENTE una canción
@app.patch("/api/songs/{id}", response_model=SongResponse)
def update_partial(id: int, song_dto: SongPatch, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # actualiza SÓLO los campos que se han enviado (no son None)
    if song_dto.title is not None:
        if not song_dto.title.strip():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la canción no puede estar vacío"
        )
        song.title = song_dto.title.strip()
    
    if song_dto.artist is not None:
        if not song_dto.artist.strip():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
        song.artist = song_dto.artist.strip()
    
    if song_dto.duration_seconds is not None:
        if song_dto.duration_seconds < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La duración debe ser un número positivo"
            )
        song.duration_seconds = song_dto.duration_seconds
    
    if song_dto.explicit is not None:
        song.explicit = song_dto.explicit
    
    db.commit() # confirma los cambios en base datos
    db.refresh(song) # refresca el objeto
    return song
"""