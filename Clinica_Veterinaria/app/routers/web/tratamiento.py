from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates import templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.tratamiento import Tratamiento
from app.models.mascota import Mascota


router = APIRouter(prefix="/tratamientos", tags=["web"])


@router.get("/", response_class=HTMLResponse)
def lista_tratamientos(request: Request, db: Session = Depends(get_db)):
    tratamientos = db.execute(select(Tratamiento)).scalars().all()
    return templates.TemplateResponse(
        "tratamientos/list.html",
        {"request": request, "tratamientos": tratamientos}
    )


@router.get("/nuevo", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    mascotas = db.execute(select(Mascota)).scalars().all()
    return templates.TemplateResponse(
        "tratamientos/form.html",
        {"request": request, "tratamiento": None, "mascotas": mascotas}
    )


@router.post("/nuevo", response_class=HTMLResponse)
def crear_tratamiento(
    request: Request,
    nombre: str = Form(...),
    costo: float = Form(...),
    tipo: str = Form(...),
    descripcion: str = Form(""),
    duracion: str = Form(...),
    ingreso: str = Form(""),
    mascota_id: int = Form(...),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "nombre": nombre,
        "costo": costo,
        "tipo": tipo,
        "descripcion": descripcion,
        "duracion": duracion,
        "ingreso": ingreso,
        "mascota_id": mascota_id
    }

    # convertir ingreso a booleano
    ingreso_value = None
    if ingreso == "true":
        ingreso_value = True
    elif ingreso == "false":
        ingreso_value = False

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if costo is None or (isinstance(costo, (int, float)) and costo < 0):
        errors.append("El costo no puede ser negativo")
    if not tipo.strip():
        errors.append("El tipo es obligatorio")
    if not duracion.strip():
        errors.append("La duración es obligatoria")

    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id)).scalar_one_or_none()
    if not mascota:
        errors.append("La mascota seleccionada no existe")

    if errors:
        mascotas = db.execute(select(Mascota)).scalars().all()
        return templates.TemplateResponse(
            "tratamientos/form.html",
            {"request": request, "tratamiento": None, "errors": errors, "form_data": form_data, "mascotas": mascotas}
        )

    try:
        tratamiento = Tratamiento(
            nombre=nombre.strip(),
            costo=costo,
            tipo=tipo.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            duracion=duracion.strip(),
            ingreso=ingreso_value,
            mascota_id=mascota_id
        )
        db.add(tratamiento)
        db.commit()
        db.refresh(tratamiento)
        return RedirectResponse(url=f"/tratamientos/{tratamiento.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear el tratamiento: {str(e)}")
        mascotas = db.execute(select(Mascota)).scalars().all()
        return templates.TemplateResponse(
            "tratamientos/form.html",
            {"request": request, "tratamiento": None, "errors": errors, "form_data": form_data, "mascotas": mascotas}
        )


@router.get("/{tratamiento_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, tratamiento_id: int, db: Session = Depends(get_db)):
    tratamiento = db.execute(select(Tratamiento).where(Tratamiento.id == tratamiento_id)).scalar_one_or_none()
    if tratamiento is None:
        raise HTTPException(status_code=404, detail="404 - Tratamiento no encontrado")

    mascotas = db.execute(select(Mascota)).scalars().all()
    return templates.TemplateResponse(
        "tratamientos/form.html",
        {"request": request, "tratamiento": tratamiento, "mascotas": mascotas}
    )


@router.post("/{tratamiento_id}/edit", response_class=HTMLResponse)
def update_tratamiento(
    request: Request,
    tratamiento_id: int,
    nombre: str = Form(...),
    costo: float = Form(...),
    tipo: str = Form(...),
    descripcion: str = Form(""),
    duracion: str = Form(...),
    ingreso: str = Form(""),
    mascota_id: int = Form(...),
    db: Session = Depends(get_db)
):
    tratamiento = db.execute(select(Tratamiento).where(Tratamiento.id == tratamiento_id)).scalar_one_or_none()
    if tratamiento is None:
        raise HTTPException(status_code=404, detail="404 - Tratamiento no encontrado")

    errors = []
    form_data = {
        "nombre": nombre,
        "costo": costo,
        "tipo": tipo,
        "descripcion": descripcion,
        "duracion": duracion,
        "ingreso": ingreso,
        "mascota_id": mascota_id
    }

    ingreso_value = None
    if ingreso == "true":
        ingreso_value = True
    elif ingreso == "false":
        ingreso_value = False

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if costo is None or (isinstance(costo, (int, float)) and costo < 0):
        errors.append("El costo no puede ser negativo")
    if not tipo.strip():
        errors.append("El tipo es obligatorio")
    if not duracion.strip():
        errors.append("La duración es obligatoria")

    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id)).scalar_one_or_none()
    if not mascota:
        errors.append("La mascota seleccionada no existe")

    if errors:
        mascotas = db.execute(select(Mascota)).scalars().all()
        return templates.TemplateResponse(
            "tratamientos/form.html",
            {"request": request, "tratamiento": None, "errors": errors, "form_data": form_data, "mascotas": mascotas}
        )

    try:
        tratamiento.nombre = nombre.strip()
        tratamiento.costo = costo
        tratamiento.tipo = tipo.strip()
        tratamiento.descripcion = descripcion.strip() if descripcion else None
        tratamiento.duracion = duracion.strip()
        tratamiento.ingreso = ingreso_value
        tratamiento.mascota_id = mascota_id

        db.commit()
        db.refresh(tratamiento)
        return RedirectResponse(url=f"/tratamientos/{tratamiento.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar el tratamiento: {str(e)}")
        mascotas = db.execute(select(Mascota)).scalars().all()
        return templates.TemplateResponse(
            "tratamientos/form.html",
            {"request": request, "tratamiento": None, "errors": errors, "form_data": form_data, "mascotas": mascotas}
        )


@router.get("/{tratamiento_id}", response_class=HTMLResponse)
def detalle_tratamiento(tratamiento_id: int, request: Request, db: Session = Depends(get_db)):
    tratamiento = db.execute(select(Tratamiento).where(Tratamiento.id == tratamiento_id)).scalar_one_or_none()
    if tratamiento is None:
        raise HTTPException(status_code=404, detail="404 - Tratamiento no registrado")

    mascota = db.execute(select(Mascota).where(Mascota.id == tratamiento.mascota_id)).scalar_one_or_none()
    return templates.TemplateResponse(
        "tratamientos/detail.html",
        {"request": request, "tratamiento": tratamiento, "mascota": mascota}
    )


@router.post("/{tratamiento_id}/eliminar", response_class=HTMLResponse)
def eliminar_tratamiento(request: Request, tratamiento_id: int, db: Session = Depends(get_db)):
    tratamiento = db.execute(select(Tratamiento).where(Tratamiento.id == tratamiento_id)).scalar_one_or_none()
    if tratamiento is None:
        raise HTTPException(status_code=404, detail="404 - Tratamiento no encontrado")
    try:
        db.delete(tratamiento)
        db.commit()
        return RedirectResponse("/tratamientos", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar el tratamiento: {str(e)}")

