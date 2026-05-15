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

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user
from app.modules.usuarios.model import Usuario
from app.modules.categorias.model import CategoriaCreate, CategoriaUpdate, CategoriaPublic
from app.modules.categorias.service import CategoriaService

router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])


@router.get("/", response_model=list[CategoriaPublic])
def list_categorias(
    # Inyección de usuario autenticado (no se usa directamente → "_" convención)
    _user: Annotated[Usuario, Depends(get_current_active_user)],

    # Inyección del Unit of Work
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """
    Lista todas las categorías.

    Flujo:
    - Abre UoW (transacción)
    - Instancia el service
    - Delega lógica
    - Retorna lista serializada
    """

    with uow:  # Manejo de sesión/transacción
        service = CategoriaService(uow)  # Inyección manual del UoW
        return service.list_all()        # Delegación total


@router.get("/{categoria_id}", response_model=CategoriaPublic)
def get_categoria(
    categoria_id: int,  # Path param

    _user: Annotated[Usuario, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """
    Obtiene una categoría por ID.
    """

    with uow:
        service = CategoriaService(uow)
        return service.get_by_id(categoria_id)


@router.post(
    "/",
    response_model=CategoriaPublic,
    status_code=status.HTTP_201_CREATED  # Semántica REST correcta (creación)
)
def create_categoria(
    cat_in: CategoriaCreate,  # Body validado por Pydantic

    _user: Annotated[Usuario, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """
    Crea una nueva categoría.

    - cat_in ya llega validado
    - No hay lógica aquí → se delega al service
    """

    with uow:
        service = CategoriaService(uow)
        return service.create(cat_in)


@router.patch("/{categoria_id}", response_model=CategoriaPublic)
def update_categoria(
    categoria_id: int,
    cat_in: CategoriaUpdate,  # Input parcial (PATCH)

    _user: Annotated[Usuario, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """
    Actualiza parcialmente una categoría.
    """

    with uow:
        service = CategoriaService(uow)
        return service.update(categoria_id, cat_in)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(
    categoria_id: int,

    _user: Annotated[Usuario, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """
    Elimina una categoría.

    - 204 → no retorna contenido (correcto en REST)
    - Si falla, el service debería lanzar excepción
    """

    with uow:
        service = CategoriaService(uow)
        service.delete(categoria_id)  # No retorna nada