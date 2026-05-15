"""
Modelo de Categoría — tabla 'categoria' en PostgreSQL.

CRUD simple protegido por JWT.
Cualquier usuario autenticado puede leer; crear/editar/borrar requiere auth.
"""

from sqlmodel import SQLModel, Field


class Categoria(SQLModel, table=True):
    id:          int | None = Field(default=None, primary_key=True)
    nombre:      str        = Field(index=True, unique=True)
    descripcion: str        = Field(default="")


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
