"""
Modelo de Pedidos — Dominio 4 del ERD v5.

Gestiona las ventas, estados del pedido y detalles de productos comprados.
"""

from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.usuarios.model import Usuario
    from app.modules.producto.models import Producto


class DetallePedido(SQLModel, table=True):
    """
    Tabla intermedia para los items de un pedido.
    Guarda el precio histórico al momento de la compra.
    """
    __tablename__ = "detalle_pedido"

    pedido_id:       int   = Field(foreign_key="pedido.id", primary_key=True)
    producto_id:     int   = Field(foreign_key="producto.id", primary_key=True)
    
    cantidad:        int   = Field(nullable=False)
    precio_unitario: float = Field(nullable=False) # Precio al momento de la venta
    subtotal:        float = Field(nullable=False)

    # Relaciones
    pedido:   "Pedido"   = Relationship(back_populates="detalles")
    producto: "Producto" = Relationship()


class Pedido(SQLModel, table=True):
    """
    Entidad principal de Pedido.
    Incluye gestión de estados y auditoría.
    """
    __tablename__ = "pedido"

    id:           Optional[int] = Field(default=None, primary_key=True)
    usuario_id:   int           = Field(foreign_key="usuario.id", nullable=False)
    
    # Estados: PENDIENTE, PAGADO, EN_PREPARACION, ENVIADO, ENTREGADO, CANCELADO
    estado:       str           = Field(default="PENDIENTE", max_length=20)
    total:        float         = Field(default=0.0)
    metodo_pago:  Optional[str] = Field(default=None, max_length=20)
    notas:        Optional[str] = Field(default=None)
    
    created_at:   datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:   datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relaciones
    usuario:  "Usuario"       = Relationship(back_populates="pedidos")
    detalles: List[DetallePedido] = Relationship(back_populates="pedido")


# ─── Esquemas de Intercambio (Schemas) ───────────────────────────────────────

class DetallePedidoCreate(SQLModel):
    producto_id: int
    cantidad:    int


class PedidoCreate(SQLModel):
    detalles:    List[DetallePedidoCreate]
    metodo_pago: Optional[str] = "EFECTIVO"
    notas:       Optional[str] = None


class PedidoPublic(SQLModel):
    id:          int
    usuario_id:  int
    estado:      str
    total:       float
    metodo_pago: Optional[str]
    created_at:  datetime
    detalles:    List[DetallePedido] = []
