from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, JSON
from datetime import datetime

# Esto lo uso para evitar importaciones circulares. 
# Solo se importa para que el tipado funcione, pero no en tiempo de ejecución.
if TYPE_CHECKING:
    from app.modules.categorias.model import Categoria
    from app.modules.ingrediente.models import Ingrediente

from app.modules.producto.associations import ProductoCategoria, ProductoIngrediente


# Uso una clase Base para no repetir los campos en el modelo de creación y el de la tabla real.
class ProductoBase(SQLModel):
    nombre: str = Field(index=True, max_length=150)
    descripcion: Optional[str] = None
    # 'gt=0' significa que el precio tiene que ser mayor a cero. Validación de negocio pura.
    precio_base: float = Field(gt=0)
    # Guardo las URLs de las imágenes como una lista en formato JSON para simplificar.
    imagenes_url: List[str] = Field(default=[], sa_column=Column(JSON))
    # 'ge=0' es mayor o igual a cero. No puedo tener stock negativo.
    stock_cantidad: int = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

# Este es el modelo que se convierte en tabla en PostgreSQL
class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    # Soft Delete: No borro el producto de verdad, solo le pongo fecha de borrado.
    # Esto me sirve para no romper pedidos viejos o estadísticas.
    deleted_at: Optional[datetime] = Field(default=None)

    # RELACIONES: Uso back_populates para que SQLModel sepa cómo conectar los dos lados.
    # El 'link_model' es la tabla intermedia que definí arriba.
    categorias: List["Categoria"] = Relationship(
        back_populates="productos", 
        link_model=ProductoCategoria
    )
    ingredientes: List["Ingrediente"] = Relationship(
        back_populates="productos", 
        link_model=ProductoIngrediente
    )
