"""
Service de Categoría — lógica de negocio.

Stateless, orquesta operaciones sobre los repositorios a través del UoW.
Lanza HTTPException. No hace commit/rollback directamente.

Capa: Service
Conoce a: UoW, Repository (indirectamente vía UoW)
NO conoce a: Router

Regla de imports:
    Router → Service → UoW → Repository → Model
"""

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.categorias.model import Categoria, CategoriaCreate, CategoriaUpdate


class CategoriaService:
    """Lógica de negocio para CRUD de categorías."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def list_all(self) -> list[Categoria]:
        """Lista todas las categorías."""
        return self.uow.categorias.get_all()

    def get_by_id(self, categoria_id: int) -> Categoria:
        """Obtiene una categoría por ID o lanza 404."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        return categoria

    def create(self, cat_in: CategoriaCreate) -> Categoria:
        """Crea una nueva categoría. Nombre debe ser único."""
        if self.uow.categorias.get_by_nombre(cat_in.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una categoría con ese nombre",
            )

        categoria = Categoria.model_validate(cat_in)
        return self.uow.categorias.add(categoria)

    def update(self, categoria_id: int, cat_in: CategoriaUpdate) -> Categoria:
        """Actualización parcial de una categoría."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        update_data = cat_in.model_dump(exclude_unset=True)

        if "nombre" in update_data:
            if self.uow.categorias.exists_nombre_excluding(
                update_data["nombre"], categoria_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe una categoría con ese nombre",
                )

        for key, value in update_data.items():
            setattr(categoria, key, value)

        return self.uow.categorias.update(categoria)

    def delete(self, categoria_id: int) -> None:
        """Elimina una categoría por ID o lanza 404."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        self.uow.categorias.delete(categoria)
