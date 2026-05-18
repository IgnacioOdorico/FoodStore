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
        """Lista todas las categorías.

        Devuelve una lista de dicts serializables para evitar errores de
        DetachedInstance cuando la sesión se cierra antes de la serialización
        del `response_model` en FastAPI.
        """
        categorias = self.uow.categorias.get_all()
        return [
            {
                "id": c.id,
                "nombre": c.nombre,
                "descripcion": c.descripcion,
                "parent_id": c.padre_id,
            }
            for c in categorias
        ]

    def get_by_id(self, categoria_id: int) -> Categoria:
        """Obtiene una categoría por ID o lanza 404."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        return {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
            "parent_id": categoria.padre_id,
        }

    def create(self, cat_in: CategoriaCreate) -> Categoria:
        """Crea una nueva categoría. Nombre debe ser único."""
        if self.uow.categorias.get_by_nombre(cat_in.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una categoría con ese nombre",
            )

        # Map API schema `parent_id` to model field `padre_id` before creating
        data = cat_in.model_dump()
        if 'parent_id' in data:
            data['padre_id'] = data.pop('parent_id')
        categoria = Categoria(**data)
        created = self.uow.categorias.add(categoria)
        return {
            "id": created.id,
            "nombre": created.nombre,
            "descripcion": created.descripcion,
            "parent_id": created.padre_id,
        }

    def update(self, categoria_id: int, cat_in: CategoriaUpdate) -> Categoria:
        """Actualización parcial de una categoría."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )

        update_data = cat_in.model_dump(exclude_unset=True)
        # Map API `parent_id` -> model `padre_id` for updates
        if 'parent_id' in update_data:
            update_data['padre_id'] = update_data.pop('parent_id')

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

        updated = self.uow.categorias.update(categoria)
        return {
            "id": updated.id,
            "nombre": updated.nombre,
            "descripcion": updated.descripcion,
            "parent_id": updated.padre_id,
        }

    def delete(self, categoria_id: int) -> None:
        """Elimina una categoría por ID o lanza 404."""
        categoria = self.uow.categorias.get_by_id(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada",
            )
        self.uow.categorias.delete(categoria)
