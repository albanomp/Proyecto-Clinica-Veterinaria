from fastapi import FastAPI, Query, Header, HTTPException
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

class Mascota (BaseModel):
 nombre: str
 edad: int
 raza: str
 genero: str

class Dueño (BaseModel):
 nombre: str
 telefono: int
 direccion: Optional[str]= None
 mascota: Mascota

class Veterinario (BaseModel):
 nombre: str
 edad: int
 horario_trabajo: Optional[str]= None
 genero: Optional[str]= None
 
class Cita (BaseModel):
 mascota: Mascota
 hora: int
 horario_trabajo: Optional[str]= None
 genero: Optional[str]= None
 
class Tratamiento (BaseModel):
 nombre: str
 cantidad: int
 tiempo_toma: int
 mascota: Mascota

class CitaPatch(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None

class TratamientoPatch(BaseModel):
    nombre: Optional[str] = None
    cantidad: Optional[int] = None
    tiempo_toma: Optional[int] = None

@app.post("/mascotas")
def crear_mascotas(mascota: Mascota):
   return {
     "mascota_creada": mascota.nombre,
     "edad":mascota.edad,
     "raza": mascota.raza,
     "genero": mascota.genero
    }

@app.post("/mascotas")
async def registrar_mascota (mascota:Mascota):
  return{
        "Registro": f"Mascota {mascota.nombre} se encuentra en la base de datos correctamente",
        "Datos de la mascota": mascota.model_dump()
    }

@app.post("/dueños")
def crear_dueño(dueño: Dueño):
    nombre_dueño = dueño.nombre
    mascota_dueño = dueño.mascota
    return{
        "dueño": nombre_dueño,
        "mascota": mascota_dueño,
        "datos completos": dueño.model_dump()
    }
