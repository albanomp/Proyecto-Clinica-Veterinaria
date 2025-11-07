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

libros = [
       {"id": 1, "titulo": "El Quijote", "autor": "Cervantes"},
       {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez"},
       {"id": 3, "titulo": "1984", "autor": "Orwell"}
   ]

@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            return libro

@app.delete("/citas/{cita_id}")
def eli_libro(libro_id:int):
    for i, libro in enumerate(libros):
        if libro["id"] == libro_id:
            libro_eliminado = libros.pop(i)
            return {"mensaje": f"Libro {libro_eliminado["titulo"]} eliminado correctamente"}
    raise HTTPException(status_code=404, detail="404 - Libro no encontrado")


@app.get("/hora-actual")
def obtener_hora():
    ahora = datetime.now()
    return {
        "fecha": ahora.strftime("%Y-%m-%D"),
        "hora": ahora.strftime("%H-%M-%S"),
        "dia_semana": ahora.strftime("%A"),
        "mes": ahora.strftime("%B"),
    }