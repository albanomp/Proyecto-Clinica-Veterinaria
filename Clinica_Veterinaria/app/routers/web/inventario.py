from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
 
from app.database import get_db
from app.models.inventario import Inventario
from app.templates import templates
 
router = APIRouter(prefix="/inventario", tags=["web_inventario"])
 
 
# LISTAR INVENTARIO
@router.get("/", response_class=HTMLResponse)
def list_inventario(request: Request, db: Session = Depends(get_db)):
    items = db.execute(select(Inventario)).scalars().all()
    return templates.TemplateResponse(
        "inventario/list.html",
        {"request": request, "items": items}
    )
 
 
# FORM CREAR
@router.get("/new", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse(
        "inventario/form.html",
        {"request": request, "item": None}
    )
 
 
# CREAR
@router.post("/new")
def create_item(
    request: Request,
    nombre: str = Form(...),
    tipo: str = Form(...),
    cantidad: int = Form(...),
    precio: float = Form(None),
    fecha_caducidad: str = Form(...),
    activo: bool = Form(False),
    db: Session = Depends(get_db)
):
    item = Inventario(
        nombre=nombre,
        tipo=tipo,
        cantidad=cantidad,
        precio=precio,
        fecha_caducidad=datetime.fromisoformat(fecha_caducidad),
        activo=activo
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return RedirectResponse(url="/inventario", status_code=303)
 
 
# DETALLE
@router.get("/{item_id}", response_class=HTMLResponse)
def detail_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.execute(
        select(Inventario).where(Inventario.id == item_id)
    ).scalar_one_or_none()
 
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
 
    return templates.TemplateResponse(
        "inventario/detalle.html",
        {"request": request, "inventario": item}
    )
 
 
# FORM EDITAR
@router.get("/{item_id}/edit", response_class=HTMLResponse)
def show_edit_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = db.execute(
        select(Inventario).where(Inventario.id == item_id)
    ).scalar_one_or_none()
 
    if not item:
        raise HTTPException(status_code=404)
 
    return templates.TemplateResponse(
        "inventario/form.html",
        {"request": request, "item": item}
    )
 
 
# EDITAR
@router.post("/{item_id}/edit")
def update_item(
    item_id: int,
    nombre: str = Form(...),
    tipo: str = Form(...),
    cantidad: int = Form(...),
    precio: float = Form(None),
    fecha_caducidad: str = Form(...),
    activo: bool = Form(False),
    db: Session = Depends(get_db)
):
    item = db.execute(
        select(Inventario).where(Inventario.id == item_id)
    ).scalar_one_or_none()
 
    if not item:
        raise HTTPException(status_code=404)
 
    item.nombre = nombre
    item.tipo = tipo
    item.cantidad = cantidad
    item.precio = precio
    item.fecha_caducidad = datetime.fromisoformat(fecha_caducidad)
    item.activo = activo
 
    db.commit()
    return RedirectResponse(url=f"/inventario/{item.id}", status_code=303)
 
 
# ELIMINAR
@router.post("/{item_id}/delete")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.execute(
        select(Inventario).where(Inventario.id == item_id)
    ).scalar_one_or_none()
 
    if not item:
        raise HTTPException(status_code=404)
 
    db.delete(item)
    db.commit()
    return RedirectResponse(url="/inventario", status_code=303)