"""
Configuración de la base de datos
"""

from sqlalchemy.orm import DeclarativeBase, sessionmaker
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

def init_db():
    from app.models import Mascota, Veterinario
    Base.metadata.create_all(engine)
    db=Sessionlocal()
    try:
        mascota_registrada=db.execute(select(Mascota)).scalars().all()
        if mascota_registrada:
            return
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


def get_db():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
