from datetime import datetime
from fastapi import APIRouter, Form, HTTPException, Request, Depends
#from Clinica_Veterinaria.app.routers.web import veterinarios
from app.templates import templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.database import get_db
from app.models import Cita, Veterinario, Mascota

#router para rutas web
router = APIRouter(prefix="/citas", tags= ["web"])

# Listar citas (http://localhost:8000/citas)
@router.get("", response_class=HTMLResponse)
def lista_de_citas(request: Request, db: Session = Depends(get_db)):
    citas = db.execute(select(Cita).options(selectinload(Cita.veterinario))).scalars().all()

    return templates.TemplateResponse(
        "citas/list.html",
        {"request" : request, "citas": citas}
    )

# mostrar formulario crear
@router.get("/new", response_class=HTMLResponse)
def mostrar_formul_creado(request: Request, db: Session = Depends(get_db)):
    veterinarios = db.execute(select(Veterinario)).scalars().all()
    mascotas = db.execute(select(Mascota)).scalars().all()

    return templates.TemplateResponse(
        "citas/form.html",
        {"request" : request, "citas" : None, "veterinarios": veterinarios, "mascotas": mascotas}
    )

# crear nueva cita
@router.post("/new", response_class=HTMLResponse)
def crear_cita(
    request: Request,
    fecha_hora: str = Form(...),
    motivo: str = Form(...),
    veterinario_id: str = Form(...),
    mascota_id: str = Form(...),
    db: Session = Depends(get_db)
):
    
    errors = []
    form_data={
        "fecha_hora": fecha_hora,
        "motivo": motivo,
        "veterinario_id": veterinario_id,
        "mascota_id": mascota_id
    }

    # validar y convertir fecha_hora
    fecha_hora_value = None
    if fecha_hora and fecha_hora.strip():

        # 1. Convertir string a datetime
        try:
            # El formato que envía <input type="datetime-local" tedría que ser YYYY-MM-DDTHH:MM
            fecha_hora_value = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors.append("La fecha de la cita tiene que tener el formato YYYY-MM-DDThh:mm")
            # raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DDThh:mm")
    if fecha_hora_value and fecha_hora_value < datetime.now():
        errors.append("La fecha de la cita no tiene que ser del pasado")
        # raise HTTPException(status_code=400, detail="No puede ser una fecha del pasado")

    if not motivo or not motivo.strip():
        errors.append("El motivo es requerido")
        # raise HTTPException(status_code=400, detail="El motivo es Requerido")

    # validar y convertir veterinario_id
    veterinario_id_value = None

    if veterinario_id and veterinario_id.strip():

        # 1. Convertir string a int
        try:
            # El formato que envía <input type="veterinario_id-local" tedría que ser un integer
            veterinario_id_value = int(veterinario_id)
        except ValueError:
            errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")
            # raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")
    if veterinario_id_value and veterinario_id_value <= 0 :
        errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")
        # raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")

    # validar y convertir mascota_id
    mascota_id_value = None

    if mascota_id and mascota_id.strip():

        # 1. Convertir string a int
        try:
            # El formato que envía <input type="veterinario_id-local" tedría que ser un integer
            mascota_id_value = int(mascota_id)
        except ValueError:
            errors.append("La mascota_id tiene que ser un numero entero positivo > 0")
            # raise HTTPException(status_code=400, detail="La mascota_id tiene que ser un numero entero positivo > 0")
    if mascota_id_value and mascota_id_value <= 0 :
        errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")

        #raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")
    """
    veterinario = db.execute(select(Veterinario).where(Veterinario.id == veterinario_id_value)).scalar_one_or_none()
    if not veterinario:
        errors.append("El veterinario seleccionado no existe")

    mascota = db.execute(select(Mascota).where(Mascota.id == mascota_id_value)).scalar_one_or_none()
    if not mascota:
        errors.append("La mascota seleccionada no existe")
    """

    veterinarios = db.execute(select(Veterinario)).scalars().all()
    mascotas = db.execute(select(Mascota)).scalars().all()

    if errors:
        return templates.TemplateResponse(
            "citas/form.html",
            {"request": request, "cita": None, "errors": errors, "veterinarios": veterinarios, "mascotas": mascotas, "form_data": form_data}
            )
    
    try:
        cita = Cita(
            fecha_hora = fecha_hora_value,
            motivo = motivo.strip(),
            veterinario_id = veterinario_id_value,
            mascota_id = mascota_id_value
        )
        db.add(cita)
        db.commit()
        db.refresh(cita)

        return RedirectResponse(url=f"/citas/{cita.id}", status_code=303)
    except Exception as e:
        db.rollback()
        errors.append(f"Error al crear la cita: {str(e)}")
    
        return templates.TemplateResponse(
            "citas/form.html",
            {"request": request, "cita": None, "errors": errors, "form_data": form_data, "veterinarios": veterinarios, "mascotas": mascotas}
        )
    
# detalle de cita (http://localhost:8000/citas/3)
@router.get("/{cita_id}", response_class=HTMLResponse)
def cita_detail(request: Request,cita_id: int, db: Session = Depends(get_db)):
    cita = db.execute(select(Cita).where(Cita.id == cita_id)).scalar_one_or_none()

    if cita is None:
        raise HTTPException(status_code=404, detail="Error 404 Cita no encontrada")
    
    veterinarios = db.execute(select(Veterinario)).scalars().all()
    mascotas = db.execute(select(Mascota)).scalars().all()


    return templates.TemplateResponse("citas/detail.html",{ "request": request, "cita": cita, "veterinarios": veterinarios, "mascotas": mascotas}
    )

# mostrar formulario editar
@router.get("/{cita_id}/edit", response_class=HTMLResponse)
def mostrar_editor_formulario(request: Request, cita_id: int, db: Session = Depends(get_db)):
    # obtener cita por id
    cita = db.execute(select(Cita).where(Cita.id == cita_id)).scalar_one_or_none()

    # lanzar error 404 si no existe cita
    if cita is None:
        raise HTTPException(status_code=404, detail="404 - la cita no ha sido encontrada")
    
    veterinarios = db.execute(select(Veterinario)).scalars().all()
    mascotas = db.execute(select(Mascota)).scalars().all()


    return templates.TemplateResponse(
        "citas/form.html",
        {"request": request , "cita": cita, "veterinarios": veterinarios, "mascotas": mascotas}
    )

# editar cita existente
@router.post("/{cita_id}/edit", response_class=HTMLResponse)
async def actualizar_cita(
    request: Request,
    cita_id: int,
    fecha_hora: str = Form(...),
    motivo: str = Form(...),
    veterinario_id: str = Form(...),
    mascota_id: str = Form(...),
    db: Session = Depends(get_db)
):
    # debug: capture raw form data to inspect what the browser actually sends
    form = await request.form()
    print("DEBUG - FORM DATA:", dict(form))
    cita = db.execute(select(Cita).where(Cita.id == cita_id)).scalar_one_or_none()

    if cita is None:
        raise HTTPException(status_code=404, detail="404 - La cita no ha sido encontrada")
    
    errors = []
    form_data ={

        "fecha_hora": fecha_hora,
        "motivo": motivo,
        "veterinario_id": veterinario_id,
        "mascota_id": mascota_id
    }

        # validar y convertir fecha_hora
    fecha_hora_value = None
    if fecha_hora and fecha_hora.strip():

        # 1. Convertir string a datetime
        try:
            # El formato que envía <input type="datetime-local" tedría que ser YYYY-MM-DDTHH:MM
            fecha_hora_value = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M")
        except ValueError:
            errors.append("La fecha de la cita tiene que tener el formato YYYY-MM-DDThh:mm")
            # raise HTTPException(status_code=400, detail="Formato de fecha inválido. Usa YYYY-MM-DDThh:mm")
    if fecha_hora_value and fecha_hora_value < datetime.now():
        errors.append("La fecha de la cita no tiene que ser del pasado")
        # raise HTTPException(status_code=400, detail="No puede ser una fecha del pasado")

    if not motivo or not motivo.strip():
        errors.append("El motivo es requerido")
        # raise HTTPException(status_code=400, detail="El motivo es Requerido")

    # validar y convertir veterinario_id
    veterinario_id_value = None

    if veterinario_id and veterinario_id.strip():

        # 1. Convertir string a int
        try:
            # El formato que envía <input type="veterinario_id-local" tedría que ser un integer
            veterinario_id_value = int(veterinario_id)
        except ValueError:
            errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")
            # raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")
    if veterinario_id_value and veterinario_id_value <= 0 :
        errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")
        # raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")

    # validar y convertir mascota_id
    mascota_id_value = None

    if mascota_id and mascota_id.strip():

        # 1. Convertir string a int
        try:
            # El formato que envía <input type="veterinario_id-local" tedría que ser un integer
            mascota_id_value = int(mascota_id)
        except ValueError:
            errors.append("La mascota_id tiene que ser un numero entero positivo > 0")
            # raise HTTPException(status_code=400, detail="La mascota_id tiene que ser un numero entero positivo > 0")
    if mascota_id_value and mascota_id_value <= 0 :
        errors.append("El vetrinario_id tiene que ser un numero entero positivo > 0")

        #raise HTTPException(status_code=400, detail="El vetrinario_id tiene que ser un numero entero positivo > 0")
        
    """
        # NOTA comentar a Maria if errors
        Comprobar longitud if len(errors):
    
    veterinario = db.execute(select(Veterinario).where(Veterinario.id == veterinario_id_value)).scalar_one_or_none()
    if not veterinario:
        errors.append("El veterinario seleccionado no existe")
    """

    if errors:
        veterinarios = db.execute(select(Veterinario)).scalars().all()
        mascotas = db.execute(select(Mascota)).scalars().all()


        return templates.TemplateResponse(
            "citas/form.html",
            {"request": request, "cita": None, "errors": errors, "form_data": form_data, "veterinarios": veterinarios, "mascotas": mascotas, "raw_form": dict(form)}
        )
    
    try:
        cita.fecha_hora = fecha_hora_value
        cita.motivo = motivo.strip()
        cita.veterinario_id = veterinario_id_value
        cita.mascota_id = mascota_id_value
        
        db.commit()
        db.refresh(cita)

        # redirigir la pantalla a detalle
        return RedirectResponse(url=f"/citas/{cita.id}", status_code=303)
    except Exception as e:
        # deshacer los cambios y añadir el error a la lista de errores
        db.rollback()
        errors.append(f"Error al actualizar la cita: {str(e)}")
        veterinarios = db.execute(select(Veterinario)).scalars().all()
        mascotas = db.execute(select(Mascota)).scalars().all()


        # devolver al formulario de edición
        return templates.TemplateResponse(
            "citas/form.html", {"request": request, "cita": cita, "errors": errors, "form_data": form_data, "veterinarios":veterinarios, "mascotas": mascotas, "raw_form": dict(form)}
        )
    
# eliminar cita
@router.post("/{cita_id}/delete", response_class=HTMLResponse)
def borrar_cita(request: Request, cita_id: int, db: Session = Depends(get_db)):
    # obtenemos la cita en base de datos
    cita = db.execute(select(Cita).options(selectinload(Cita.veterinario)).where(Cita.id == cita_id)).scalar_one_or_none()
    
    # si no hay cita lanzar una excepción
    if cita is None:
        raise HTTPException(status_code=404, detail="404 - La cita no ha sido encontrada")
    
    # eliminar la cita
    try:
        db.delete(cita)
        db.commit()

        # redirigir a la lista de citas
        return RedirectResponse(url="/citas", status_code=303)
    except Exception as e:
        # deshacemos los cambios si da error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la cita: {str(e)}")