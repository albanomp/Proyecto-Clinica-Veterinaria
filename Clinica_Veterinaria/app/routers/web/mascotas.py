from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates import templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models import Mascota, Duenyo
from app.database import get_db


router = APIRouter(prefix="/mascotas", tags=["web"])


@router.get("/", response_class=HTMLResponse)
def lista_mascota(request: Request, db: Session = Depends(get_db)):
    mascotas = db.execute(select(Mascota).options(selectinload(Mascota.duenyo))).scalars().all()
    return templates.TemplateResponse(
        "mascotas/list.html",
        {"request": request, "mascotas": mascotas}
    )


@router.get("/nuevo", response_class=HTMLResponse)
def show_create_form(request: Request, db: Session = Depends(get_db)):
    duenyos = db.execute(select(Duenyo)).scalars().all()
    return templates.TemplateResponse(
        "mascotas/form.html",
        {"request": request, "duenyos": duenyos}
    )

@router.post("/nuevo", response_class=HTMLResponse)
def crear_mascota(
    request: Request,
    nombre: str = Form(...),
    especie: str = Form(...),
    raza: str = Form(...),
    fecha_nacimiento: str = Form(...),
    chip: str = Form(""),
    duenyo_id: int = Form(...),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "fecha_nacimiento": fecha_nacimiento,
        "chip": chip,
        "duenyo_id": duenyo_id
    }

    chip_value = None
    if chip == "true":
        chip_value = True
    elif chip == "false":
        chip_value = False

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if not especie.strip():
        errors.append("La especie es obligatoria")
    if not raza.strip():
        errors.append("La raza es obligatoria")
    if not fecha_nacimiento.strip():
        errors.append("La fecha de nacimiento es obligatoria")
    
    duenyo = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()
    if not duenyo:
        errors.append("El dueño seleccionado no existe")

    if errors:
        return templates.TemplateResponse(
            "mascotas/form.html",
            {"request": request, "mascota": None, "errors": errors, "form_data": form_data, "duenyos": duenyos}
        )

    try:
        mascota = Mascota(
            nombre=nombre.strip(),
            especie=especie.strip(),
            raza=raza.strip(),
            fecha_nacimiento=fecha_nacimiento.strip(),
            chip=chip_value,
            duenyo_id=duenyo_id

        )
        db.add(mascota)
        db.commit()
        db.refresh(mascota)
        return RedirectResponse(url=f"/mascotas/{mascota.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la mascota: {str(e)}")
        duenyos = db.execute(select(Duenyo)).scalars().all()
        return templates.TemplateResponse(
            "mascotas/form.html",
            {"request": request, "mascota": None, "errors": errors, "form_data": form_data, "duenyos": duenyos}
        )



@router.get("/{mascota_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id)).scalar_one_or_none()

    if mascota is None:
        raise HTTPException(status_code=404, detail="404 - Mascota no encontrada")
    
    duenyos = db.execute(select(Duenyo)).scalars().all()

    return templates.TemplateResponse(
        "mascotas/form.html",
        {"request": request, "mascota": mascota, "duenyos": duenyos}
    )


@router.post("/{mascota_id}/edit", response_class=HTMLResponse)
def update_mascota(
    request: Request,
    mascota_id: int,
    nombre: str = Form(...),
    especie: str = Form(...),
    raza: str = Form(...),
    fecha_nacimiento: str = Form(...),
    chip: str = Form(""),
    duenyo_id: int = Form(...),
    db: Session = Depends(get_db)
):
    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id)).scalar_one_or_none()
    if mascota is None:
        raise HTTPException(status_code=404, detail="404 - Mascota no encontrada")

    errors = []
    form_data = {
        "nombre": nombre,
        "especie": especie,
        "raza": raza,
        "fecha_nacimiento": fecha_nacimiento,
        "chip": chip,
        "duenyo_id": duenyo_id
    }

    chip_value = None
    if chip == "true":
        chip_value = True
    elif chip == "false":
        chip_value = False

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if not especie.strip():
        errors.append("La especie es obligatoria")
    if not raza.strip():
        errors.append("La raza es obligatoria")
    if not fecha_nacimiento.strip():
        errors.append("La fecha de nacimiento es obligatoria")
    
    duenyo = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()
    if not duenyo:
        errors.append("El dueño seleccionado no existe")

    if errors:
        duenyos = db.execute(select(Duenyo)).scalars().all()
        return templates.TemplateResponse(
            "mascotas/form.html",
            {"request": request, "mascota": None, "errors": errors, "form_data": form_data, "duenyos": duenyos}
        )

    try:
        mascota.nombre = nombre.strip()
        mascota.especie = especie.strip()
        mascota.raza = raza.strip()
        mascota.fecha_nacimiento = fecha_nacimiento.strip()
        mascota.chip = chip_value
        mascota.duenyo_id = duenyo_id

        db.commit()
        db.refresh(mascota)
        return RedirectResponse(url=f"/mascotas/{mascota.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar la mascota: {str(e)}")
        duenyos = db.execute(select(Duenyo)).scalars().all()
        return templates.TemplateResponse(
            "mascotas/form.html",
            {"request": request, "mascota": None, "errors": errors, "form_data": form_data, "duenyos": duenyos}
        )



@router.get("/{mascota_id}", response_class=HTMLResponse)
def detalle_mascota(mascota_id: int, request: Request, db: Session = Depends(get_db)):
    mascota = db.execute(select(Mascota).options(selectinload(Mascota.duenyo)).where(Mascota.id == mascota_id)).scalar_one_or_none()
    if mascota is None:
        raise HTTPException(status_code=404, detail="404 - Mascota no registrada")
    return templates.TemplateResponse(
        "mascotas/detalle.html",
        {"request": request, "mascota": mascota}
    )



@router.post("/{mascota_id}/eliminar", response_class=HTMLResponse)
def eliminar_mascota(request: Request, mascota_id: int, db: Session = Depends(get_db)):
    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id)).scalar_one_or_none()
    if mascota is None:
        raise HTTPException(status_code=404, detail="404 - Mascota no encontrada")
    try:
        db.delete(mascota)
        db.commit()
        return RedirectResponse("/mascotas", status_code=303)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la mascota: {str(e)}")
    