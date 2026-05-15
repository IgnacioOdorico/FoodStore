"""
Repositorio de Pedidos.

Acceso a BD para órdenes y sus detalles.
"""

from typing import List, Optional
from sqlmodel import Session, select
from app.core.base_repository import BaseRepository
from app.modules.pedidos.models import Pedido, DetallePedido


class PedidoRepository(BaseRepository[Pedido]):
    def __init__(self, session: Session):
        super().__init__(Pedido, session)

    def get_by_usuario(self, usuario_id: int) -> List[Pedido]:
        """Obtiene el historial de pedidos de un usuario."""
        return list(self.session.exec(
            select(Pedido).where(Pedido.usuario_id == usuario_id)
        ).all())

    def get_by_estado(self, estado: str) -> List[Pedido]:
        """Filtra pedidos por su estado (ej: 'PENDIENTE')."""
        return list(self.session.exec(
            select(Pedido).where(Pedido.estado == estado)
        ).all())


class DetallePedidoRepository(BaseRepository[DetallePedido]):
    def __init__(self, session: Session):
        super().__init__(DetallePedido, session)
