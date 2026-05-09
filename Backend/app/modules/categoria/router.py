"""
Router CRUD de Categorías.

HTTP puro: parsear request, validar schema Pydantic, delegar al Service,
serializar response con response_model. No contiene lógica de negocio.

Capa: Router
Conoce a: Service (vía UoW)
NO conoce a: Repository, Model (solo esquemas para response_model)

Regla de imports:
    Router → Service → UoW → Repository → Model
"""

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user
from app.modules.usuarios.models import Usuario
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead, CategoriaReadWithChildren
from app.modules.categoria.service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/", response_model=List[CategoriaRead])
def list_categorias(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    parent_only: Annotated[bool, Query(description="Solo categorías raíz")] = False,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    """Lista las categorías. Permite filtrar por nombre o mostrar solo las raíz."""
    with uow:
        service = CategoriaService(uow)
        return service.list_categorias(nombre=nombre, parent_only=parent_only)


@router.post("/", response_model=CategoriaRead)
def create_categoria(
    data: CategoriaCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = CategoriaService(uow)
        return service.create_categoria(data)


@router.get("/{id}", response_model=CategoriaRead)
def get_categoria(
    id: int,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = CategoriaService(uow)
        categoria = service.get_categoria(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@router.put("/{id}", response_model=CategoriaRead)
def update_categoria(
    id: int,
    data: CategoriaUpdate,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = CategoriaService(uow)
        categoria = service.update_categoria(id, data)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@router.delete("/{id}")
def delete_categoria(
    id: int,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = CategoriaService(uow)
        success = service.delete_categoria(id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return {"message": "Categoria eliminada"}
