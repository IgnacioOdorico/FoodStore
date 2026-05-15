"""
Router CRUD de Ingredientes.

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
from app.modules.ingrediente.schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead
from app.modules.ingrediente.service import IngredienteService

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.get("/", response_model=List[IngredienteRead])
def list_ingredientes(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    es_alergeno: Annotated[Optional[bool], Query(description="Filtrar por alérgenos")] = None,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = IngredienteService(uow)
        return service.list_ingredientes(nombre=nombre, es_alergeno=es_alergeno)


@router.post("/", response_model=IngredienteRead)
def create_ingrediente(
    data: IngredienteCreate,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = IngredienteService(uow)
        return service.create_ingrediente(data)


@router.get("/{id}", response_model=IngredienteRead)
def get_ingrediente(
    id: int,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = IngredienteService(uow)
        ingrediente = service.get_ingrediente(id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.put("/{id}", response_model=IngredienteRead)
def update_ingrediente(
    id: int,
    data: IngredienteUpdate,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = IngredienteService(uow)
        ingrediente = service.update_ingrediente(id, data)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


@router.delete("/{id}")
def delete_ingrediente(
    id: int,
    _user: Annotated[Usuario, Depends(get_current_active_user)] = None,
    uow: Annotated[UnitOfWork, Depends(get_uow)] = None,
):
    with uow:
        service = IngredienteService(uow)
        success = service.delete_ingrediente(id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return {"message": "Ingrediente eliminado"}
