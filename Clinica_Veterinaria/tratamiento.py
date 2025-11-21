from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, select, Integer, String, Boolean, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker, Session
from pydantic import BaseModel, ConfigDict
from enum import Enum

engine = create_engine(
    "sqlite:///tratamientos.db",
    echo=False,
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


class TipoTratamiento(str, Enum):
    vacuna = "vacuna"
    medicamento = "medicamento"
    cirugia = "cirugia"
    estetico = "estetico"
    otro = "otro"


class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    costo: Mapped[float] = mapped_column(Float, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    duracion: Mapped[str] = mapped_column(String(100), nullable=False)
    ingreso: Mapped[bool] = mapped_column(Boolean, default=False)


Base.metadata.create_all(engine)

def init_db():
    db = SessionLocal()
    try:
        existing = db.execute(select(Tratamiento)).scalars().all()
        if existing:
            return

        default_tr = [
            Tratamiento(
                nombre="Vacuna antirrábica",
                costo=45.0,
                tipo="vacuna",
                descripcion="Vacuna anual para protección de la rabia.",
                duracion="1 año",
                ingreso=False
            ),
            Tratamiento(
                nombre="Limpieza dental",
                costo=120.0,
                tipo="estetico",
                descripcion="Limpieza dental completa bajo sedación.",
                duracion="2 horas",
                ingreso=True
            ),
            Tratamiento(
                nombre="Antibiótico en comprimidos",
                costo=22.5,
                tipo="medicamento",
                descripcion="Antibiótico de amplio espectro por herida infectada.",
                duracion="7 días",
                ingreso=False
            )
        ]

        db.add_all(default_tr)
        db.commit()
    finally:
        db.close()


init_db()


class TratamientoCreate(BaseModel):
    nombre: str
    costo: float = 0.0
    tipo: TipoTratamiento = TipoTratamiento.otro
    descripcion: str = ""
    duracion: str = "1 día"
    ingreso: bool = False


class TratamientoUpdate(BaseModel):
    nombre: str
    costo: float
    tipo: TipoTratamiento
    descripcion: str
    duracion: str
    ingreso: bool


class TratamientoPatch(BaseModel):
    nombre: str | None = None
    costo: float | None = None
    tipo: TipoTratamiento | None = None
    descripcion: str | None = None
    duracion: str | None = None
    ingreso: bool | None = None


class TratamientoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    costo: float
    tipo: str
    descripcion: str
    duracion: str
    ingreso: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Gestión de Tratamientos Veterinarios")

@app.get("/api/tratamientos", response_model=list[TratamientoResponse])
def find_all(db: Session = Depends(get_db)):
    return db.execute(select(Tratamiento)).scalars().all()


@app.get("/api/tratamientos/{id}", response_model=TratamientoResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    tr = db.execute(select(Tratamiento).where(Tratamiento.id == id)).scalar_one_or_none()
    if not tr:
        raise HTTPException(404, f"Tratamiento con ID {id} no encontrado")
    return tr


@app.post("/api/tratamientos", response_model=TratamientoResponse, status_code=201)
def create(tr_dto: TratamientoCreate, db: Session = Depends(get_db)):

    if tr_dto.costo < 0:
        raise HTTPException(400, "El costo no puede ser negativo")

    nuevo = Tratamiento(
        nombre=tr_dto.nombre,
        costo=tr_dto.costo,
        tipo=tr_dto.tipo.value,
        descripcion=tr_dto.descripcion,
        duracion=tr_dto.duracion,
        ingreso=tr_dto.ingreso
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@app.patch("/api/tratamientos/{id}", response_model=TratamientoResponse)
def patch(id: int, tr_dto: TratamientoPatch, db: Session = Depends(get_db)):

    tr = db.execute(select(Tratamiento).where(Tratamiento.id == id)).scalar_one_or_none()
    if not tr:
        raise HTTPException(404, f"Tratamiento con ID {id} no encontrado")

    if tr_dto.nombre is not None:
        tr.nombre = tr_dto.nombre

    if tr_dto.costo is not None:
        if tr_dto.costo < 0:
            raise HTTPException(400, "El costo no puede ser negativo")
        tr.costo = tr_dto.costo

    if tr_dto.tipo is not None:
        tr.tipo = tr_dto.tipo.value

    if tr_dto.descripcion is not None:
        tr.descripcion = tr_dto.descripcion

    if tr_dto.duracion is not None:
        tr.duracion = tr_dto.duracion

    if tr_dto.ingreso is not None:
        tr.ingreso = tr_dto.ingreso

    db.commit()
    db.refresh(tr)

    return tr


@app.delete("/api/tratamientos/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    tr = db.execute(select(Tratamiento).where(Tratamiento.id == id)).scalar_one_or_none()

    if not tr:
        raise HTTPException(404, f"Tratamiento con ID {id} no encontrado")

    db.delete(tr)
    db.commit()

    return None
