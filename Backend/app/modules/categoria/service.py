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

from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from sqlmodel import select

from app.core.uow import UnitOfWork
from app.modules.categoria.models import Categoria
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead


class CategoriaService:
    """Lógica de negocio para CRUD de categorías."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def list_categorias(self, nombre: str = None, parent_only: bool = False) -> list:
        """Lista las categorías con filtros opcionales."""
        statement = select(Categoria).where(Categoria.deleted_at == None)  # noqa: E711
        if nombre:
            statement = statement.where(Categoria.nombre.contains(nombre))
        if parent_only:
            statement = statement.where(Categoria.parent_id == None)  # noqa: E711
        items = self.uow.session.exec(statement).all()
        return [CategoriaRead.model_validate(i) for i in items]

    def create_categoria(self, data: CategoriaCreate) -> CategoriaRead:
        """Crea una nueva categoría."""
        categoria = Categoria(**data.model_dump())
        self.uow.categorias.add(categoria)
        return CategoriaRead.model_validate(categoria)

    def get_categoria(self, id: int) -> CategoriaRead | None:
        """Obtiene una categoría por ID o retorna None."""
        categoria = self.uow.session.get(Categoria, id)
        if not categoria or categoria.deleted_at:
            return None
        return CategoriaRead.model_validate(categoria)

    def update_categoria(self, id: int, data: CategoriaUpdate) -> CategoriaRead | None:
        """Actualización parcial de una categoría."""
        categoria = self.uow.session.get(Categoria, id)
        if not categoria or categoria.deleted_at:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(categoria, key, value)

        self.uow.categorias.update(categoria)
        return CategoriaRead.model_validate(categoria)

    def delete_categoria(self, id: int) -> bool:
        """Soft delete de una categoría y sus descendientes."""
        all_ids = self._get_descendant_ids(id)
        now = datetime.now()

        for cid in all_ids:
            cat = self.uow.session.get(Categoria, cid)
            if cat:
                cat.deleted_at = now
                self.uow.session.add(cat)

        # Soft delete de productos asociados
        from app.modules.producto.models import Producto, ProductoCategoria
        statement = select(Producto).join(ProductoCategoria).where(
            ProductoCategoria.categoria_id.in_(all_ids),
            Producto.deleted_at == None,  # noqa: E711
        )
        products_to_delete = self.uow.session.exec(statement).all()
        for prod in products_to_delete:
            prod.deleted_at = now
            self.uow.session.add(prod)

        return True

    def _get_descendant_ids(self, category_id: int) -> List[int]:
        """Obtiene recursivamente todos los IDs de descendientes."""
        all_ids = [category_id]
        to_process = [category_id]
        while to_process:
            curr_id = to_process.pop()
            statement = select(Categoria).where(
                Categoria.parent_id == curr_id,
                Categoria.deleted_at == None,  # noqa: E711
            )
            children = self.uow.session.exec(statement).all()
            for child in children:
                if child.id not in all_ids:
                    all_ids.append(child.id)
                    to_process.append(child.id)
        return all_ids

    def get_descendant_ids(self, category_id: int) -> List[int]:
        """Obtiene recursivamente todos los IDs de descendientes (API pública)."""
        return self._get_descendant_ids(category_id)
