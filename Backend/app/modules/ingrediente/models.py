from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.modules.producto.models import Producto
from app.modules.producto.associations import ProductoIngrediente

class Ingrediente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=100)
    descripcion: Optional[str] = None
    es_alergeno: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    productos: List["Producto"] = Relationship(
        back_populates="ingredientes", 
        link_model=ProductoIngrediente
    )
