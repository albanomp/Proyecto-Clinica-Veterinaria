"""
Configuración de la base de datos
"""

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, select

engine = create_engine(
    "sqlite:///Mascotas.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

Sessionlocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


def init_db():
    
    from app.models import Mascota, Veterinario, Duenyo, Tratamiento

   
    Base.metadata.create_all(engine)

    db = Sessionlocal()
    try:
       
        veterinarios = db.execute(select(Veterinario)).scalars().all()
        mascotas = db.execute(select(Mascota)).scalars().all()

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
                Mascota(nombre="Alejandro", especie="tortuga", raza="estrellada", fecha_nacimiento="11-09-2001", chip=True),
                Mascota(nombre="Balboa", especie="Perro", raza="Pastor alemán", fecha_nacimiento="28-11-2018", chip=False),
                Mascota(nombre="Carlos", especie="Ave", raza="Grajilla", fecha_nacimiento="16-03-2021", chip=True),
                Mascota(nombre="Deme", especie="Reptil", raza="Serpiente Boa", fecha_nacimiento="7-01-2016", chip=False),
                Mascota(nombre="Elena", especie="Gato", raza="negro", fecha_nacimiento="17-07-2023", chip=True),
                Mascota(nombre="Fabricio", especie="Ave", raza="Pájaro Carpintero", fecha_nacimiento="19-09-2024", chip=True),
                Mascota(nombre="Gabriel", especie="Reptil", raza="Dragón de Komodo", fecha_nacimiento="30-08-2015", chip=False),
            ]
            db.add_all(default_mascotas)
            db.commit()

     
        duenyos = db.execute(select(Duenyo)).scalars().all()

        if not duenyos:
            default_duenos = [
                Duenyo(nombre="Paola", telefono="612345678", email="paola80@gmail.com", direccion="Calle Los Olivos 23"),
                Duenyo(nombre="Carlos", telefono="678912345", email="carlos79@gmail.com", direccion="Av. Gran Canaria 45"),
                Duenyo(nombre="Lucía", telefono="698745632", email="lucia98@gmail.com", direccion="Calle San Sebastián 12"),
                Duenyo(nombre="Kevin", telefono="657893221", email="kevin91@gmail.com", direccion="Calle Jerusalén 66"),
                Duenyo(nombre="Samira", telefono="676356579", email="samira_93@gmail.com", direccion="Av.del Cabildo 57"),
                Duenyo(nombre="Roberto", telefono="722345987", email="roberto@gmail.com", direccion="Calle Hebanista 34"),
                Duenyo(nombre="Antonia", telefono="928576576", email="", direccion=""),
            ]
            db.add_all(default_duenos)
            db.commit()


        tratamientos = db.execute(select(Tratamiento)).scalars().all()

        if not tratamientos:
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


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

