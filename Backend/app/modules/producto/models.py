"""
Modelo de Producto — tabla 'producto' en PostgreSQL.

Adaptado al ERD v5:
  - imagen_url (singular), sin stock_cantidad (se maneja por ingredientes).
"""

from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria
    from app.modules.ingrediente.models import Ingrediente

from app.modules.producto.associations import ProductoCategoria, ProductoIngrediente


class Producto(SQLModel, table=True):
    __tablename__ = "producto"

    id:            Optional[int] = Field(default=None, primary_key=True)
    nombre:        str           = Field(index=True, max_length=100, nullable=False)
    descripcion:   Optional[str] = Field(default=None)
    precio_base:   float         = Field(nullable=False) # NUMERIC(12,2)
    imagen_url:    Optional[str] = Field(default=None, max_length=255)
    disponible:    bool          = Field(default=True)
    
    # Audit
    created_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at:    Optional[datetime] = Field(default=None)

    # Relaciones N:N
    categorias: List["Categoria"] = Relationship(
        back_populates="productos", 
        link_model=ProductoCategoria
    )
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos", 
        link_model=ProductoIngrediente
    )


# ─── Esquemas Pydantic ───────────────────────────────────────────────────────

class ProductoCreate(SQLModel):
    nombre:        str = Field(min_length=1, max_length=100)
    descripcion:   Optional[str] = None
    precio_base:   float = Field(gt=0)
    imagen_url:    Optional[str] = None
    disponible:    bool = True


class ProductoPublic(SQLModel):
    id:            int
    nombre:        str
    descripcion:   Optional[str]
    precio_base:   float
    imagen_url:    Optional[str]
    disponible:    bool
    created_at:    datetime
