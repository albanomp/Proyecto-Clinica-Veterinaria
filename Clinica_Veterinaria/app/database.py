"""
Configuración de la base de datos
"""

from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# -------------------------
# Engine y sesión
# -------------------------

engine = create_engine(
    "sqlite:///Clínica.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

Sessionlocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


# -------------------------
# Base declarativa
# -------------------------

class Base(DeclarativeBase):
    pass


# -------------------------
# Inicialización de la BD
# -------------------------

def init_db():

    from app.models import (
        Mascota,
        Veterinario,
        Duenyo,
        Tratamiento,
        Cita,
        Inventario,
    )

    # Crear tablas
    Base.metadata.create_all(engine)

    db = Sessionlocal()

    try:

        duenyos = db.execute(select(Duenyo)).scalars().all()
        veterinarios = db.execute(select(Veterinario)).scalars().all()
        mascotas = db.execute(select(Mascota)).scalars().all()
        tratamientos = db.execute(select(Tratamiento)).scalars().all()
        inventario = db.execute(select(Inventario)).scalars().all()
        citas = db.execute(select(Cita)).scalars().all()

        if not duenyos:
            default_duenos = [
                Duenyo(nombre="Paola", telefono="612345678", email="paola80@gmail.com", direccion="Calle Los Olivos 23"),
                Duenyo(nombre="Carlos", telefono="678912345", email="carlos79@gmail.com", direccion="Av. Gran Canaria 45"),
                Duenyo(nombre="Lucía", telefono="698745632", email="lucia98@gmail.com", direccion="Calle San Sebastián 12"),
                Duenyo(nombre="Kevin", telefono="657893221", email="kevin91@gmail.com", direccion="Calle Jerusalén 66"),
                Duenyo(nombre="Samira", telefono="676356579", email="samira_93@gmail.com", direccion="Av. del Cabildo 57"),
                Duenyo(nombre="Roberto", telefono="722345987", email="roberto@gmail.com", direccion="Calle Hebanista 34"),
                Duenyo(nombre="Antonia", telefono="928576576", email="", direccion=""),
            ]
            db.add_all(default_duenos)
            db.commit()

        if not veterinarios:
            default_vets = [
                Veterinario(nombre="Albano", colegiado=12345, especialidad="Reptiles", telefono=666890121),
                Veterinario(nombre="Borja", colegiado=11346, especialidad="Mamiferos", telefono=654761015),
                Veterinario(nombre="Carlota", colegiado=15925, especialidad="Oviparos", telefono=672315692),
                Veterinario(nombre="Estefania", colegiado=21674, especialidad="Inyecciones", telefono=612362891),
            ]
            db.add_all(default_vets)
            db.commit()

        if not mascotas:
            default_mascotas = [
                Mascota(nombre="Alejandro", especie="tortuga", raza="estrellada", fecha_nacimiento="11-09-2001", chip=True, duenyo_id=1),
                Mascota(nombre="Balboa", especie="Perro", raza="Pastor alemán", fecha_nacimiento="28-11-2018", chip=False, duenyo_id=3),
                Mascota(nombre="Carlos", especie="Ave", raza="Grajilla", fecha_nacimiento="16-03-2021", chip=True, duenyo_id=2),
                Mascota(nombre="Deme", especie="Reptil", raza="Serpiente Boa", fecha_nacimiento="7-01-2016", chip=False, duenyo_id=2),
                Mascota(nombre="Elena", especie="Gato", raza="negro", fecha_nacimiento="17-07-2023", chip=True, duenyo_id=4),
                Mascota(nombre="Fabricio", especie="Ave", raza="Pájaro Carpintero", fecha_nacimiento="19-09-2024", chip=True, duenyo_id=5),
                Mascota(nombre="Gabriel", especie="Reptil", raza="Dragón de Komodo", fecha_nacimiento="30-08-2015", chip=False, duenyo_id=6),
            ]
            db.add_all(default_mascotas)
            db.commit()


        if not tratamientos:
            default_tratamientos = [
                Tratamiento(
                    nombre="Vacuna antirrábica",
                    costo=45.0,
                    tipo="vacuna",
                    descripcion="Vacuna anual para protección de la rabia.",
                    duracion="1 año",
                    ingreso=False,
                    mascota_id=1,
                ),
                Tratamiento(
                    nombre="Limpieza dental",
                    costo=120.0,
                    tipo="estetico",
                    descripcion="Limpieza dental completa bajo sedación.",
                    duracion="2 horas",
                    ingreso=True,
                    mascota_id=2,
                ),
                Tratamiento(
                    nombre="Antibiótico en comprimidos",
                    costo=22.5,
                    tipo="medicamento",
                    descripcion="Antibiótico de amplio espectro por herida infectada.",
                    duracion="7 días",
                    ingreso=False,
                    mascota_id=5,
                ),
            ]
            db.add_all(default_tratamientos)
            db.commit()

        if not inventario:
            default_inventario = [
                Inventario(
                    nombre="Vacuna antirrábica",
                    tipo="medicamento",
                    cantidad=50,
                    precio=12.5,
                    fecha_caducidad=datetime(2026, 6, 1),
                    activo=True,
                ),
                Inventario(
                    nombre="Antibiótico canino",
                    tipo="medicamento",
                    cantidad=30,
                    precio=8.9,
                    fecha_caducidad=datetime(2025, 11, 15),
                    activo=True,
                ),
                Inventario(
                    nombre="Guantes desechables",
                    tipo="material",
                    cantidad=200,
                    precio=None,
                    fecha_caducidad=datetime(2030, 1, 1),
                    activo=True,
                ),
            ]
            db.add_all(default_inventario)
            db.commit()

        if not citas:
            default_citas = [
                Cita(fecha_hora=datetime(2025, 12, 14, 10, 30), motivo="Vacunación", veterinario_id=1, mascota_id=3),
                Cita(fecha_hora=datetime(2025, 12, 23, 11, 0), motivo="Revisión", veterinario_id=2, mascota_id=1),
                Cita(fecha_hora=datetime(2025, 12, 21, 9, 30), motivo="Vacunación", veterinario_id=2, mascota_id=4),
                Cita(fecha_hora=datetime(2025, 12, 16, 10, 30), motivo="Visita Inicial", veterinario_id=2, mascota_id=2),
                Cita(fecha_hora=datetime(2025, 12, 17, 10, 30), motivo="Tratamiento", veterinario_id=2, mascota_id=5),
                Cita(fecha_hora=datetime(2025, 12, 19, 9, 30), motivo="Vacunación", veterinario_id=1, mascota_id=6),
                Cita(fecha_hora=datetime(2025, 12, 19, 12, 30), motivo="Vacunación", veterinario_id=1, mascota_id=7),
            ]
            db.add_all(default_citas)
            db.commit()

    finally:
        db.close()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
