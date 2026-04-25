from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.modules.producto.models import Producto
from app.modules.producto.models import ProductoCategoria

class CategoriaBase(SQLModel):
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relaciones
    parent: Optional["Categoria"] = Relationship(
        back_populates="children", 
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    children: List["Categoria"] = Relationship(back_populates="parent")
    productos: List["Producto"] = Relationship(
        back_populates="categorias", 
        link_model=ProductoCategoria
    )
