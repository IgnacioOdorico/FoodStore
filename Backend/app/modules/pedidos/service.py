"""
Service de Pedidos — lógica de negocio y FSM.

Orquesta la creación de órdenes, cálculo de totales y transiciones de estado.
"""

from typing import List
from fastapi import HTTPException, status
from app.core.uow import UnitOfWork
from app.modules.pedidos.models import Pedido, DetallePedido, PedidoCreate, PedidoPublic


class PedidoService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def crear_pedido(self, usuario_id: int, data: PedidoCreate) -> PedidoPublic:
        """
        Crea un nuevo pedido, calcula el total basándose en los precios actuales
        de los productos y persiste los detalles.
        """
        # 1. Crear la cabecera del pedido
        pedido = Pedido(
            usuario_id=usuario_id,
            metodo_pago=data.metodo_pago,
            notas=data.notas,
            estado="PENDIENTE"
        )
        self.uow.pedidos.add(pedido)
        self.uow.session.flush() # Para obtener el ID del pedido

        total_acumulado = 0.0

        # 2. Procesar detalles
        for item in data.detalles:
            producto = self.uow.productos.get_by_id(item.producto_id)
            if not producto or producto.deleted_at:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {item.producto_id} no encontrado"
                )
            
            if not producto.disponible:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El producto '{producto.nombre}' no está disponible"
                )

            subtotal = producto.precio_base * item.cantidad
            
            detalle = DetallePedido(
                pedido_id=pedido.id,
                producto_id=producto.id,
                cantidad=item.cantidad,
                precio_unitario=producto.precio_base,
                subtotal=subtotal
            )
            self.uow.session.add(detalle)
            total_acumulado += subtotal

        # 3. Actualizar total final
        pedido.total = total_acumulado
        self.uow.pedidos.update(pedido)
        
        return self._to_public(pedido)

    def cambiar_estado(self, pedido_id: int, nuevo_estado: str) -> PedidoPublic:
        """Gestiona la transición de estados del pedido."""
        pedido = self.uow.pedidos.get_by_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        # Validar estados permitidos según ERD v5
        ESTADOS_VALIDOS = ["PENDIENTE", "PAGADO", "EN_PREPARACION", "ENVIADO", "ENTREGADO", "CANCELADO"]
        if nuevo_estado not in ESTADOS_VALIDOS:
            raise HTTPException(status_code=400, detail=f"Estado '{nuevo_estado}' no es válido")

        pedido.estado = nuevo_estado
        self.uow.pedidos.update(pedido)
        return self._to_public(pedido)

    def listar_por_usuario(self, usuario_id: int) -> List[PedidoPublic]:
        pedidos = self.uow.pedidos.get_by_usuario(usuario_id)
        return [self._to_public(p) for p in pedidos]

    def _to_public(self, pedido: Pedido) -> PedidoPublic:
        return PedidoPublic.model_validate(pedido)
