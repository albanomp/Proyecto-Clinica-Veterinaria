"""
Endpoints de apirest (CRUD)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.schemas import ActualizarMascota, CrearMascota, ParcheMascota, RespuestaMascota
from app.database import get_db
from app.models import Mascota

router = APIRouter(prefix="/api", tags=["Mascotas"])


@router.get("/mascotas",response_model=list[RespuestaMascota])
def todas_las_mascotas(db:Session=Depends(get_db)):
    return db.execute(select(Mascota)).scalars().all()


@router.get("/encontrar_mascota/{id}",response_model=RespuestaMascota)
def una_mascota(id: int, db:Session=Depends(get_db)):
 mascota= db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
 if not mascota:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= "404- Mascota no encontrada")
 return mascota

@router.post("/crear_mascota", response_model=CrearMascota, status_code= status.HTTP_201_CREATED)
def create(mascota_dto: CrearMascota,db:Session=Depends(get_db)):
    if not mascota_dto.nombre.strip():
        raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
    if not mascota_dto.especie.strip():
        raise HTTPException(status_code=400, detail= "La especie no puede estar vacío")
    if not mascota_dto.raza.strip():
        raise HTTPException(status_code=400, detail= "La raza no puede estar vacío")
    if not mascota_dto.fecha_nacimiento.strip():
        raise HTTPException(status_code=400, detail= "La fecha no puede estar vacía")
    mascota_dto=Mascota(
        nombre= mascota_dto.nombre.strip(), especie= mascota_dto.especie.strip(), 
        raza= mascota_dto.raza.strip(),fecha_nacimiento= mascota_dto.fecha_nacimiento.strip(), 
        chip= mascota_dto.chip,
        duenyo_id=mascota_dto.duenyo_id
        )
    db.add(mascota_dto)
    db.commit()
    db.refresh(mascota_dto)
    return mascota_dto

@router.put("/actualizar_mascota/{id}", response_model=ActualizarMascota)
def update(id:int, mascota_dto: ActualizarMascota,db:Session=Depends(get_db)):
    mascota_dto = db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
    if not mascota_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado la mascota con id {id}"
        )
    if not mascota_dto.nombre.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre no puede estar vacío."
        )       
        
    if not mascota_dto.especie.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La especie no puede estar vacío."
        )    
    
    if not mascota_dto.raza.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La raza no puede estar vacía."
        )
    if not mascota_dto.fecha_nacimiento.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha no puede estar vacía."
        )        

    mascota_dto.nombre= mascota_dto.nombre.strip()
    mascota_dto.especie= mascota_dto.especie.strip()
    mascota_dto.raza= mascota_dto.raza.strip()
    mascota_dto.fecha_nacimiento= mascota_dto.fecha_nacimiento.strip()
    mascota_dto.chip= mascota_dto.chip
    mascota_dto.duenyo_id = mascota_dto.duenyo_id
    
    db.commit()
    db.refresh(mascota_dto)
    return mascota_dto

@router.delete("/eliminar_mascota/{id}",status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mascota(id: int, db:Session=Depends(get_db)):
    mascota=db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
    if not mascota:
     raise HTTPException(status_code=404, detail= "404- Mascota registrada no encontrada")
    db.delete(mascota)
    db.commit()
    return None


@router.patch("/parchear_mascota", response_model=ParcheMascota)
def parche(id:int, mascota_dto: ParcheMascota,db:Session=Depends(get_db)):
    mascota= db.execute(select(Mascota).where(Mascota.id == id)).scalar_one_or_none()
    
    if not mascota_dto:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= f"404- Mascota con {id} no encontrada")
 
    if mascota_dto.nombre is not None:
        if not mascota_dto.nombre.strip():
         raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
        mascota.nombre = mascota_dto.nombre.strip()
    
    if mascota_dto.especie is not None:
        if not mascota_dto.especie.strip():
         raise HTTPException(status_code=400, detail= "La especie no puede estar vacía")
        mascota.especie = mascota_dto.especie.strip()
    
    
    if mascota_dto.raza is not None:
        if not mascota_dto.raza.strip():
         raise HTTPException(status_code=400, detail= "La raza no puede estar vacía")
        mascota.raza = mascota_dto.raza.strip()
    
    if mascota_dto.fecha_nacimiento is not None:
        if not mascota_dto.fecha_nacimiento.strip():
         raise HTTPException(status_code=400, detail= "La fecha no puede estar vacía")
        mascota.fecha_nacimiento = mascota_dto.fecha_nacimiento.strip()
    
    if mascota_dto.duenyo_id is not None:
        if not mascota_dto.duenyo_id.strip():
         raise HTTPException(status_code=400, detail= "La fecha no puede estar vacía")# 🔥 OPCIONAL
        mascota.duenyo_id = mascota_dto.duenyo_id
    
    
    db.commit()
    db.refresh(mascota)
    return mascota
#uvicorn Mascotas:app  --reload
#http://127.0.0.1:8000