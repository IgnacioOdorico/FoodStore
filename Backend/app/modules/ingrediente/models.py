"""
Modelo de Ingrediente — tabla 'ingrediente' en PostgreSQL.

Adaptado al ERD v5:
  - unidad_medida, stock_actual, stock_minimo.
"""

from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.producto.models import Producto

from app.modules.producto.associations import ProductoIngrediente


class Ingrediente(SQLModel, table=True):
    id:            Optional[int] = Field(default=None, primary_key=True)
    nombre:        str           = Field(index=True, unique=True, max_length=100, nullable=False)
    unidad_medida: str           = Field(max_length=20, nullable=False) # ej: "g", "ml", "un"
    
    stock_actual:  float         = Field(default=0.0) # NUMERIC(12,3)
    stock_minimo:  float         = Field(default=0.0)
    
    # Podés mantener es_alergeno si lo usás en el front, pero el ERD no lo tiene.
    # Lo dejaré para no romper lógica existente si la hay.
    es_alergeno:   bool          = Field(default=False)
    
    created_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relación N:N con Producto
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes", 
        link_model=ProductoIngrediente
    )


# ─── Esquemas Pydantic ───────────────────────────────────────────────────────

class IngredienteCreate(SQLModel):
    nombre:        str = Field(min_length=1, max_length=100)
    unidad_medida: str = Field(min_length=1, max_length=20)
    stock_minimo:  float = 0.0
    es_alergeno:   bool = False


class IngredientePublic(SQLModel):
    id:            int
    nombre:        str
    unidad_medida: str
    stock_actual:  float
    stock_minimo:  float
    es_alergeno:   bool
