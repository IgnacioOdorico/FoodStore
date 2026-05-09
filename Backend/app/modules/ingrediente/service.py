"""
Service de Ingrediente — lógica de negocio.

Stateless, orquesta operaciones sobre los repositorios a través del UoW.
Lanza HTTPException. No hace commit/rollback directamente.

Capa: Service
Conoce a: UoW, Repository (indirectamente vía UoW)
NO conoce a: Router
"""

from sqlmodel import select

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.ingrediente.models import Ingrediente
from app.modules.ingrediente.schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead


class IngredienteService:
    """Lógica de negocio para CRUD de ingredientes."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def list_ingredientes(self, nombre: str = None, es_alergeno: bool = None) -> list:
        """Lista ingredientes con filtros opcionales."""
        statement = select(Ingrediente)
        if nombre:
            statement = statement.where(Ingrediente.nombre.contains(nombre))
        if es_alergeno is not None:
            statement = statement.where(Ingrediente.es_alergeno == es_alergeno)
        items = self.uow.session.exec(statement).all()
        return [IngredienteRead.model_validate(i) for i in items]

    def create_ingrediente(self, data: IngredienteCreate) -> IngredienteRead:
        """Crea un nuevo ingrediente."""
        ingrediente = Ingrediente(**data.model_dump())
        self.uow.ingredientes.add(ingrediente)
        return IngredienteRead.model_validate(ingrediente)

    def get_ingrediente(self, id: int) -> IngredienteRead | None:
        """Obtiene un ingrediente por ID."""
        ingrediente = self.uow.ingredientes.get_by_id(id)
        return IngredienteRead.model_validate(ingrediente) if ingrediente else None

    def update_ingrediente(self, id: int, data: IngredienteUpdate) -> IngredienteRead | None:
        """Actualización parcial de un ingrediente."""
        ingrediente = self.uow.ingredientes.get_by_id(id)
        if not ingrediente:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(ingrediente, key, value)

        self.uow.ingredientes.update(ingrediente)
        return IngredienteRead.model_validate(ingrediente)

    def delete_ingrediente(self, id: int) -> bool:
        """Soft delete de un ingrediente."""
        ingrediente = self.uow.ingredientes.get_by_id(id)
        if not ingrediente:
            return False
        from datetime import datetime
        ingrediente.deleted_at = datetime.now() if hasattr(ingrediente, 'deleted_at') else None
        self.uow.session.delete(ingrediente)
        return True
