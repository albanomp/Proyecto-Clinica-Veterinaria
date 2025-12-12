from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas import duenyo
from app.database import get_db
from app.models import Duenyo
from app.models.mascota import Mascota   # ⬅ IMPORTANTE: añadimos Mascota

templates = Jinja2Templates(directory="Clinica_veterinaria/app/templates")

router = APIRouter(prefix="/duenyos", tags=["web_duenyos"])

@router.get("", response_class=HTMLResponse)
def list_duenyos(request: Request, db: Session = Depends(get_db)):
    duenyos = db.execute(select(Duenyo)).scalars().all()
    
    return templates.TemplateResponse(
        "duenyos/list.html",
        {"request": request, "duenyos": duenyos}
    )

@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "duenyos/form.html",
        {"request": request, "duenyo": None}
    )

@router.post("/new", response_class=HTMLResponse)
def create_duenyo(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    errors = []
    form_data = {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "direccion": direccion
    }

    if not nombre or not nombre.strip():
        errors.append("El nombre es obligatorio.")
    if not apellido or not apellido.strip():
        errors.append("El apellido es obligatorio.")

    if errors:
        return templates.TemplateResponse(
            "duenyos/form.html",
            {"request": request, "dueno": None, "errors": errors, "form_data": form_data}
        )

    try:
        dueno = Duenyo(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None
        )

        db.add(dueno)
        db.commit()
        db.refresh(dueno)

        return RedirectResponse(url=f"/duenyos/{dueno.id}", status_code=303)

    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear: {str(e)}")
        return templates.TemplateResponse(
            "duenyos/form.html",
            {"request": request, "duenyo": None, "errors": errors, "form_data": form_data}
        )

@router.get("/{duenyo_id}", response_class=HTMLResponse)
def dueno_detail(request: Request, duenyo_id: int, db: Session = Depends(get_db)):
    dueno = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()

    if dueno is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    # ⭐ OBTENER LAS MASCOTAS QUE PERTENECEN A ESTE DUEÑO
    mascotas = db.execute(
        select(Mascota).where(Mascota.duenyo_id == duenyo_id)
    ).scalars().all()

    return templates.TemplateResponse(
        "duenyos/detail.html",
        {
            "request": request,
            "duenyo": dueno,
            "mascotas": mascotas   # ⭐ PASAMOS LA LISTA DE MASCOTAS
        }
    )

@router.get("/{duenyo_id}/edit", response_class=HTMLResponse)
def show_edit_form(request: Request, duenyo_id: int, db: Session = Depends(get_db)):
    dueno = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()

    if dueno is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    return templates.TemplateResponse(
        "duenyos/form.html",
        {"request": request, "dueno": dueno}
    )

@router.post("/{duenyo_id}/edit", response_class=HTMLResponse)
def update_duenyo(
    request: Request,
    duenyo_id: int,
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(None),
    direccion: str = Form(None),
    db: Session = Depends(get_db)
):
    dueno = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()

    if dueno is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    errors = []

    if not nombre.strip():
        errors.append("El nombre es obligatorio")
    if not apellido.strip():
        errors.append("El apellido es obligatorio")

    if errors:
        return templates.TemplateResponse(
            "duenyos/form.html",
            {"request": request, "duenyo": dueno, "errors": errors}
        )

    try:
        dueno.nombre = nombre.strip()
        dueno.apellido = apellido.strip()
        dueno.telefono = telefono.strip() if telefono else None
        dueno.direccion = direccion.strip() if direccion else None

        db.commit()
        db.refresh(dueno)

        return RedirectResponse(url=f"/duenyos/{dueno.id}", status_code=303)

    except Exception as e:
        db.rollback()
        errors.append(f"Error al actualizar: {str(e)}")
        return templates.TemplateResponse(
            "duenyos/form.html",
            {"request": request, "duenyo": dueno, "errors": errors}
        )

@router.post("/{duenyo_id}/delete")
def delete_duenyo(request: Request, duenyo_id: int, db: Session = Depends(get_db)):
    duenyo = db.execute(select(Duenyo).where(Duenyo.id == duenyo_id)).scalar_one_or_none()

    if duenyo is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")

    try:
        db.delete(duenyo)
        db.commit()

        return RedirectResponse(url="/duenyos", status_code=303)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar: {str(e)}")
