from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.schemas import ActualizarVeterinario, CrearVeterinario, ParcheVeterinario, RespuestaVeterinario
from app.database import get_db
from app.models import Veterinario

router = APIRouter(prefix="/api", tags=["Veterinarios"])

@router.get("/veterinarios",response_model=list[RespuestaVeterinario])
def todos_las_veterinarios(db:Session=Depends(get_db)):
    return db.execute(select(Veterinario)).scalars().all()


@router.get("/encontrar_veterinario/{id}",response_model=RespuestaVeterinario)
def un_veterinario(id: int, db:Session=Depends(get_db)):
 veterinario= db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
 if not veterinario:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= "404- Veterinario no encontrada")
 return veterinario

@router.post("/crear_veterinario", response_model=CrearVeterinario, status_code= status.HTTP_201_CREATED)
def create(veterinario_dto: CrearVeterinario,db:Session=Depends(get_db)):
    if not veterinario_dto.colegiado.strip():
        raise HTTPException(status_code=400, detail= "El colegiado no puede estar vacío")
    if not veterinario_dto.telefono.strip():
        raise HTTPException(status_code=400, detail= "El telefono no puede estar vacío")
    veterinario_dto=Veterinario(
        nombre= veterinario_dto.nombre.strip(), colegiado= veterinario_dto.colegiado.strip(), 
        especialidad= veterinario_dto.especialidad.strip(),telefono= veterinario_dto.telefono.strip()
        )
    db.add(veterinario_dto)
    db.commit()
    db.refresh(veterinario_dto)
    return veterinario_dto

@router.put("/actualizar_veterinario/{id}", response_model=ActualizarVeterinario)
def update(id:int, veterinario_dto: ActualizarVeterinario,db:Session=Depends(get_db)):
    veterinario_dto = db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    if not veterinario_dto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se ha encontrado el veterinario con id {id}"
        )    

    if not veterinario_dto.telefono.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El telefono no puede estar vacío."
        )        

    veterinario_dto.nombre= veterinario_dto.nombre.strip()
    veterinario_dto.colegiado= veterinario_dto.colegiado.strip()
    veterinario_dto.especialidad= veterinario_dto.especialidad.strip()
    veterinario_dto.telefono= veterinario_dto.telefono.strip()
    
    db.commit()
    db.refresh(veterinario_dto)
    return veterinario_dto



@router.patch("/parchear_veterinario", response_model=ParcheVeterinario)
def parche(id:int, veterinario_dto: ParcheVeterinario,db:Session=Depends(get_db)):
    veterinario= db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    
    if not veterinario_dto:
     #status.HTTP_404_NOT_FOUND
     raise HTTPException(status_code=404, detail= f"404- Veterinario con {id} no encontrado")
 
    if veterinario_dto.nombre is not None:
        if not veterinario_dto.nombre.strip():
         raise HTTPException(status_code=400, detail= "El nombre no puede estar vacío")
        veterinario.nombre = veterinario_dto.nombre.strip()
    
    if veterinario_dto.colegiado is not None:
        if not veterinario_dto.colegiado.strip():
         raise HTTPException(status_code=400, detail= "El colegiado no puede estar vacío")
        veterinario.colegiado = veterinario_dto.colegiado.strip()
    
    
    if veterinario_dto.especialidad is not None:
        if not veterinario_dto.raza.strip():
         raise HTTPException(status_code=400, detail= "La especialidad no puede estar vacía")
        veterinario.especialidad = veterinario_dto.especialidad.strip()
    
    if veterinario_dto.telefono is not None:
        if not veterinario_dto.telefono.strip():
         raise HTTPException(status_code=400, detail= "El telefono no puede estar vacío")
        veterinario.telefono = veterinario_dto.telefono.strip()
    
    
    db.commit()
    db.refresh(veterinario)
    return veterinario


@router.delete("/eliminar_veterinario/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_veterinario(id: int, db:Session=Depends(get_db)):
    veterinario=db.execute(select(Veterinario).where(Veterinario.id == id)).scalar_one_or_none()
    if not veterinario:
     raise HTTPException(status_code=404, detail= "404- Veterinario ya no trabaja aqui")
    db.delete(veterinario)
    db.commit()
    return None