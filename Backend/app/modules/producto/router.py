from fastapi import APIRouter, HTTPException, Query
from typing import List, Annotated, Optional
from app.modules.producto.service import ProductoService
from app.modules.producto.schemas import ProductoCreate, ProductoUpdate, ProductoRead, ProductoReadWithDetails

router = APIRouter(prefix="/productos", tags=["Productos"])
service = ProductoService()

@router.get("/", response_model=List[ProductoReadWithDetails])
def list_productos(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por disponibilidad")] = None,
    categoria_id: Annotated[Optional[int], Query(description="Filtrar por categoría")] = None
):
    return service.list_productos(nombre=nombre, disponible=disponible, categoria_id=categoria_id)

@router.post("/", response_model=ProductoReadWithDetails)
def create_producto(data: ProductoCreate):
    return service.create_producto(data)

@router.get("/{id}", response_model=ProductoReadWithDetails)
def get_producto(id: int):
    producto = service.get_producto(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{id}", response_model=ProductoReadWithDetails)
def update_producto(id: int, data: ProductoUpdate):
    producto = service.update_producto(id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{id}")
def delete_producto(id: int):
    success = service.delete_producto(id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado"}
