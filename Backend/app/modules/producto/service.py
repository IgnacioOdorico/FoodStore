"""
Service de Producto — lógica de negocio.

Stateless, orquesta operaciones sobre los repositorios a través del UoW.

Capa: Service
Conoce a: UoW, Repository (indirectamente vía UoW)
NO conoce a: Router
"""

from datetime import datetime

from sqlmodel import select
from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente
from app.modules.producto.schemas import (
    ProductoCreate,
    ProductoUpdate,
    ProductoReadWithDetails,
)


class ProductoService:
    """Lógica de negocio para CRUD de productos."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def list_productos(self, nombre: str = None, disponible: bool = None, categoria_id: int = None) -> list:
        """Lista productos activos con filtros opcionales."""
        statement = select(Producto).where(Producto.deleted_at == None)  # noqa: E711

        if nombre:
            statement = statement.where(Producto.nombre.contains(nombre))
        if disponible is not None:
            statement = statement.where(Producto.disponible == disponible)

        if categoria_id:
            from app.modules.categoria.service import CategoriaService
            cat_service = CategoriaService(self.uow)
            relevant_ids = cat_service.get_descendant_ids(categoria_id)
            statement = statement.join(ProductoCategoria).where(
                ProductoCategoria.categoria_id.in_(relevant_ids)
            )
            statement = statement.distinct()

        items = self.uow.session.exec(statement).all()
        for i in items:
            _ = i.categorias
            _ = i.ingredientes
        return [ProductoReadWithDetails.model_validate(i) for i in items]

    def create_producto(self, data: ProductoCreate) -> ProductoReadWithDetails:
        """Crea un producto con sus relaciones N:N."""
        categoria_ids = data.categoria_ids
        ingrediente_ids = data.ingrediente_ids
        prod_data = data.model_dump(exclude={"categoria_ids", "ingrediente_ids"})

        producto = Producto(**prod_data)
        self.uow.productos.add(producto)

        for cat_id in categoria_ids:
            self.uow.session.add(ProductoCategoria(producto_id=producto.id, categoria_id=cat_id, es_principal=True))
        for ing_id in ingrediente_ids:
            self.uow.session.add(ProductoIngrediente(producto_id=producto.id, ingrediente_id=ing_id))

        self.uow.session.flush()
        return self._get_with_details(producto.id)

    def get_producto(self, id: int) -> ProductoReadWithDetails | None:
        """Obtiene un producto por ID con sus relaciones."""
        producto = self.uow.productos.get_by_id(id)
        if not producto or producto.deleted_at:
            return None
        return self._get_with_details(id)

    def _get_with_details(self, id: int) -> ProductoReadWithDetails:
        """Carga las relaciones del producto y construye el DTO."""
        producto = self.uow.session.get(Producto, id)
        self.uow.session.expire(producto, ["categorias", "ingredientes"])
        dto = ProductoReadWithDetails.model_validate(producto)

        for cat_dto in dto.categorias:
            link = self.uow.session.exec(
                select(ProductoCategoria).where(
                    ProductoCategoria.producto_id == id,
                    ProductoCategoria.categoria_id == cat_dto.id,
                )
            ).first()
            if link:
                cat_dto.es_principal = link.es_principal

        for ing_dto in dto.ingredientes:
            link = self.uow.session.exec(
                select(ProductoIngrediente).where(
                    ProductoIngrediente.producto_id == id,
                    ProductoIngrediente.ingrediente_id == ing_dto.id,
                )
            ).first()
            if link:
                ing_dto.es_removible = link.es_removible

        return dto

    def update_producto(self, id: int, data: ProductoUpdate) -> ProductoReadWithDetails | None:
        """Actualización parcial de un producto."""
        producto = self.uow.productos.get_by_id(id)
        if not producto or producto.deleted_at:
            return None

        update_data = data.model_dump(exclude_unset=True, exclude={"categoria_ids", "ingrediente_ids"})
        for key, value in update_data.items():
            setattr(producto, key, value)
        producto.updated_at = datetime.now()

        if data.categoria_ids is not None:
            existing_cats = self.uow.session.exec(
                select(ProductoCategoria).where(ProductoCategoria.producto_id == id)
            ).all()
            for ec in existing_cats:
                self.uow.session.delete(ec)
            for cat_id in data.categoria_ids:
                self.uow.session.add(ProductoCategoria(producto_id=id, categoria_id=cat_id, es_principal=True))

        if data.ingrediente_ids is not None:
            existing_ings = self.uow.session.exec(
                select(ProductoIngrediente).where(ProductoIngrediente.producto_id == id)
            ).all()
            for ei in existing_ings:
                self.uow.session.delete(ei)
            for ing_id in data.ingrediente_ids:
                self.uow.session.add(ProductoIngrediente(producto_id=id, ingrediente_id=ing_id))

        self.uow.productos.update(producto)
        self.uow.session.flush()
        return self._get_with_details(id)

    def delete_producto(self, id: int) -> bool:
        """Soft delete de un producto."""
        producto = self.uow.productos.get_by_id(id)
        if not producto or producto.deleted_at:
            return False
        producto.deleted_at = datetime.now()
        self.uow.productos.update(producto)
        return True
