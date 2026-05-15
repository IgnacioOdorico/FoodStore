"""
Router de Pedidos.

Endpoints para que los clientes realicen órdenes y los administradores gestionen estados.
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.model import UserPublic
from app.modules.pedidos.models import PedidoCreate, PedidoPublic
from app.modules.pedidos.service import PedidoService

router = APIRouter(prefix="/api/v1/pedidos", tags=["pedidos"])


@router.post("/", response_model=PedidoPublic, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate,
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Crea un nuevo pedido para el usuario autenticado."""
    with uow:
        service = PedidoService(uow)
        return service.crear_pedido(current_user.id, data)


@router.get("/me", response_model=List[PedidoPublic])
def mis_pedidos(
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Historial de pedidos del cliente."""
    with uow:
        service = PedidoService(uow)
        return service.listar_por_usuario(current_user.id)


@router.patch("/{pedido_id}/estado", response_model=PedidoPublic)
def actualizar_estado(
    pedido_id: int,
    nuevo_estado: str,
    _admin: Annotated[UserPublic, Depends(require_role(["ADMIN", "PEDIDOS"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Cambia el estado de un pedido (Solo ADMIN o PEDIDOS)."""
    with uow:
        service = PedidoService(uow)
        return service.cambiar_estado(pedido_id, nuevo_estado)


@router.get("/admin/pendientes", response_model=List[PedidoPublic])
def pedidos_pendientes(
    _admin: Annotated[UserPublic, Depends(require_role(["ADMIN", "PEDIDOS"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Lista todos los pedidos pendientes de gestión."""
    with uow:
        # Podríamos añadir un método específico en service si es necesario
        return [PedidoPublic.model_validate(p) for p in uow.pedidos.get_by_estado("PENDIENTE")]
