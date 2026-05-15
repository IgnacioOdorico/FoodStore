"""
Router CRUD de Productos.

HTTP puro: parsear request, validar schema Pydantic, delegar al Service,
serializar response con response_model. No contiene lógica de negocio.

Capa: Router
Conoce a: Service (vía UoW)
NO conoce a: Repository, Model (solo esquemas para response_model)
"""

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user
from app.modules.usuarios.model import Usuario
from app.modules.producto.schemas import ProductoCreate, ProductoUpdate, ProductoReadWithDetails
from app.modules.producto.service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoReadWithDetails])
def list_productos(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    disponible: Annotated[Optional[bool], Query(description="Filtrar por disponibilidad")] = None,
    categoria_id: Annotated[Optional[int], Query(description="Filtrar por categoría")] = None,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = ProductoService(uow)
        return service.list_productos(nombre=nombre, disponible=disponible, categoria_id=categoria_id)


@router.post("/", response_model=ProductoReadWithDetails)
def create_producto(
    data: ProductoCreate,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = ProductoService(uow)
        return service.create_producto(data)


@router.get("/{id}", response_model=ProductoReadWithDetails)
def get_producto(
    id: int,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = ProductoService(uow)
        producto = service.get_producto(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{id}", response_model=ProductoReadWithDetails)
def update_producto(
    id: int,
    data: ProductoUpdate,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = ProductoService(uow)
        producto = service.update_producto(id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{id}")
def delete_producto(
    id: int,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = ProductoService(uow)
        success = service.delete_producto(id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado"}
