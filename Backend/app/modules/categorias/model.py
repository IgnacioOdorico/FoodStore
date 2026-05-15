"""
Modelo de Categoría — tabla 'categoria' en PostgreSQL.

CRUD simple protegido por JWT.
Cualquier usuario autenticado puede leer; crear/editar/borrar requiere auth.
"""

from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.producto.models import Producto

from app.modules.producto.associations import ProductoCategoria


class Categoria(SQLModel, table=True):
    id:          int | None = Field(default=None, primary_key=True)
    nombre:      str        = Field(index=True, unique=True)
    descripcion: str        = Field(default="")

    # Relación con Producto (agregada para compatibilidad con FoodStore)
    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )


# ─── Esquemas Pydantic ───────────────────────────────────────────────────────

class CategoriaCreate(SQLModel):
    """Datos para crear una categoría."""
    nombre:      str = Field(min_length=1, max_length=100)
    descripcion: str = Field(default="", max_length=500)


class CategoriaUpdate(SQLModel):
    """Datos para actualizar (parcial — todos opcionales)."""
    nombre:      str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)


class CategoriaPublic(SQLModel):
    """Vista pública de la categoría."""
    id:          int
    nombre:      str
    descripcion: str
