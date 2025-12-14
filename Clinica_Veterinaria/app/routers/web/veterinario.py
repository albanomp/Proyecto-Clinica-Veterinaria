from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates import templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Veterinario
from app.database import get_db


router= APIRouter(prefix="/veterinarios",tags=["web"])

@router.get("/", response_class=HTMLResponse)
def lista_empleado(request: Request, db:Session = Depends(get_db)):
    veterinarios = db.execute(select(Veterinario)).scalars().all()
    return templates.TemplateResponse(
        "veterinarios/list.html",
        {"request":request, "veterinarios":veterinarios}
        
    )

@router.get("/formulario", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "veterinarios/form.html",
        {"request":request}
    )

@router.post("/formulario",response_class=HTMLResponse)
def crear_veterinario(
    request: Request,
    nombre: str = Form(...),
    colegiado: str = Form(...),
    especialidad: str = Form(...),
    telefono: str = Form(...),
    db:Session = Depends(get_db)
):
    errors=[]
    form_data={
        "nombre":nombre,
        "colegiado":colegiado,
        "especialidad":especialidad,
        "telefono":telefono
    }
    
    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if not colegiado.strip():
        errors.append("El colegiado es obligatorio")
    if not especialidad.strip():
        errors.append("La especialidad es obligatoria")
    if not telefono.strip():
        errors.append("El teléfono es obligatorio")
    
    if errors:
        return templates.TemplateResponse(
        "veterinarios/form.html",
        {"request":request, "veterinario":None, "errors":errors, "form_data":form_data}
    )
    try:
        veterinario= Veterinario(
            nombre= nombre.strip(),
            colegiado= colegiado.strip(),
            especialidad= especialidad.strip(),
            telefono= telefono.strip(),
        )
        db.add(veterinario)
        db.commit()
        db.refresh(veterinario)
        return RedirectResponse(url=f"/veterinarios/{veterinario.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el empleado: {str(e)}")
        return templates.TemplateResponse(
        "veterinarios/form.html",
        {"request":request, "veterinario":None, "errors":errors, "form_data":form_data}
        ) 

@router.get("/{veterinario_id}/editar", response_class=HTMLResponse)
def show_edit_form(request: Request, veterinario_id: int, db: Session = Depends(get_db)):
    veterinario = db.execute(select(Veterinario).where(Veterinario.id == veterinario_id)).scalar_one_or_none()

    if veterinario is None:
        raise HTTPException(status_code=404, detail="404 - Veterinario no encontrada")

    return templates.TemplateResponse(
        "veterinarios/form.html",
        {"request": request, "veterinario": veterinario}
    )


@router.post("/{veterinario_id}/editar", response_class=HTMLResponse)
def update_empleado(
    request: Request,
    veterinario_id: int,
    nombre: str = Form(...),
    colegiado: str = Form(...),
    especialidad: str = Form(...),
    telefono: str = Form(...),
    db: Session = Depends(get_db)
):
    
    veterinario = db.execute(select(Veterinario).where(Veterinario.id == veterinario_id)).scalar_one_or_none()
    if veterinario is None:
        raise HTTPException(status_code=404, detail="404 - Veterinario no encontrada")


    errors = []
    form_data = {
        "nombre": nombre,
        "colegiado": colegiado,
        "especialidad": especialidad,
        "telefono": telefono
    }

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if not colegiado.strip():
        errors.append("El colegiado es obligatorio")
    if not especialidad.strip():
        errors.append("La especialidad es obligatoria")
    if not telefono.strip():
        errors.append("El teléfono es obligatorio")
    

    if errors:
        return templates.TemplateResponse(
            "veterinarios/form.html",
            {"request": request, "veterinario": None, "errors": errors, "form_data": form_data}
        )

    try:
        veterinario.nombre = nombre.strip()
        veterinario.colegiado = colegiado.strip()
        veterinario.especialidad = especialidad.strip()
        veterinario.telefono = telefono.strip()


        db.commit()
        db.refresh(veterinario)
        return RedirectResponse(url=f"/veterinarios/{veterinario.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la mascota: {str(e)}")

        return templates.TemplateResponse(
            "veterinarios/form.html",
            {"request": request, "veterinario": veterinario, "errors": errors, "form_data": form_data}
        )

@router.get("/{veterinario_id}", response_class=HTMLResponse)
def lista_mascota(veterinario_id: int, request: Request, db:Session = Depends(get_db)):
    veterinario= db.execute(select(Veterinario).where(Veterinario.id == veterinario_id)).scalar_one_or_none()
    if veterinario is None:
        raise HTTPException(status_code=404, detail= "404 - veterinario no registrado")
    return templates.TemplateResponse(
        "veterinarios/detalle.html",
        {"request":request, "veterinario":veterinario}
        
    )


@router.post("/{veterinario_id}/eliminar", response_class=HTMLResponse)
def eliminar_empleado(request: Request, veterinario_id: int, db: Session = Depends(get_db)):
    veterinario = db.execute(select(Veterinario).where(Veterinario.id == veterinario_id)).scalar_one_or_none()
    if veterinario is None:
        raise HTTPException(status_code=404, detail="404 - Veterinario no encontrado")
    try:
        db.delete(veterinario)
        db.commit()
        return RedirectResponse("/veterinarios", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar al empleado: {str(e)}")