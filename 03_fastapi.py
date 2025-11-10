"""
pip install -r requirements.txt
API REST de FastAPI con SQLAlchemy y SQLite
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Configurar base de datos
engine = create_engine('sqlite:///ecommerce.db', echo=True) # echo True para mostrar SQL solo en desarrollo
SessionLocal = sessionmaker(bind=engine)
# TODO - autoflush a true, commit true

# Crear clase Base
class Base(DeclarativeBase):
    pass

# SQLALCHEMY MODELS : crear entidades que heredan de Base (models.py)
class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

# PYDANTIC MODELS : crear schemas pydantic (schemas.py)
class ProductDTO(BaseModel):
    nombre: str | None = None

# Crear tablas
Base.metadata.create_all(engine)

# API REST FastAPI con SQLAlchemy
app = FastAPI(title='Products App', version='1.0.0')

@app.get('/')
def home():
    return {'mensaje': 'Products API'}

# API REST:
# GET all products JSON
@app.get('/api/products')
def find_all():
    session = SessionLocal()
    # opción tradicional query
    # products = session.query(Product).all()
    
    # opción moderna select
    statement = select(Product)
    products = session.execute(statement).scalars().all()
    
    session.close()
    return products

# GET one product BY ID
@app.get('/api/products/{id}')
def find_by_id(id: int):
    session = SessionLocal()
    # opción tradicional query
    # product = session.query(Product).filter(Product.id == id).first()
    
    # opción moderna
    product = session.execute(
        select(Product).where(Product.id == id)
    ).scalar_one_or_none()
    
    session.close()
    if not product:
        raise HTTPException(status_code=404, detail='Not found')
    return product


# POST create product

@app.post('/api/products', status_code=status.HTTP_201_CREATED)
def create(product_dto: ProductDTO):
    session = SessionLocal()
    product = Product(nombre=product_dto.nombre)
    session.add(product) # guardar en base de datos INSERT
    session.commit() # se guarda el producto en base de datos asignando un nuevo id
    session.refresh(product) # actualizar id de product
    session.close()
    # TODO - Gestión de errores: 
    #   si nombre está ocupado entonces lanzar un 400 bad request
    #   si precio menor que 0.01 entonces lanzar un 400 bad request
    return product


# PUT update product (actualizar un producto existente) (no crea nuevos)
@app.put('/api/products/{id}')
def update(id: int, product_dto: ProductDTO):
    session = SessionLocal()
    
    # 1. buscar el producto por id en base de datos y si no existe lanzar 404
    product = session.execute(
        select(Product).where(Product.id == id)
    ).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail='Not found')
    
    # 2. si sí existe, actualizamos el producto recuperado de base de datos
    # con los datos del product_dto
    if product_dto.nombre is not None:
        product.nombre = product_dto.nombre
        
    #if product_dto.price is not None and product_dto.price > 0.01:
    #    product.price
    # TODO actualizar todo los campos que se quiera, por ejemplo: nombre, precio, cantidad, fecha, activo
    
    session.commit()
    session.refresh(product)
    session.close()
    return product

# DELETE remove product
@app.delete('/api/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int):
    session = SessionLocal()
    
    # 1 buscar si el producto existe, si no existe devolver 404
    product = session.execute(
        select(Product).where(Product.id == id)
    ).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail='Not found')
    
    # si sí existe, borrarlo y devolver 204 no content
    session.delete(product)
    session.commit()
    session.close()
    return None
    

# HTML:
# GET all products HTML
# GET one product HTML
# POST create/update product