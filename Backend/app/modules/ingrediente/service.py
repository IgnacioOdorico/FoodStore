from sqlmodel import select
from app.modules.ingrediente.unit_of_work import IngredienteUnitOfWork
from app.modules.ingrediente.models import Ingrediente
from app.modules.ingrediente.schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead

class IngredienteService:
    def list_ingredientes(self, nombre: str = None, es_alergeno: bool = None):
        with IngredienteUnitOfWork() as uow:
            statement = select(Ingrediente)
            if nombre:
                statement = statement.where(Ingrediente.nombre.contains(nombre))
            if es_alergeno is not None:
                statement = statement.where(Ingrediente.es_alergeno == es_alergeno)
            
            items = uow.session.exec(statement).all()
            return [IngredienteRead.model_validate(i) for i in items]

    def create_ingrediente(self, data: IngredienteCreate):
        with IngredienteUnitOfWork() as uow:
            ingrediente = Ingrediente(**data.model_dump())
            uow.ingredientes.create(ingrediente)
            uow.commit()
            uow.session.refresh(ingrediente)
            return IngredienteRead.model_validate(ingrediente)

    def get_ingrediente(self, id: int):
        with IngredienteUnitOfWork() as uow:
            ingrediente = uow.ingredientes.get(id)
            return IngredienteRead.model_validate(ingrediente) if ingrediente else None

    def update_ingrediente(self, id: int, data: IngredienteUpdate):
        with IngredienteUnitOfWork() as uow:
            ingrediente = uow.ingredientes.get(id)
            if not ingrediente:
                return None
            
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(ingrediente, key, value)
            
            uow.ingredientes.update(ingrediente)
            uow.commit()
            uow.session.refresh(ingrediente)
            return IngredienteRead.model_validate(ingrediente)

    def delete_ingrediente(self, id: int):
        with IngredienteUnitOfWork() as uow:
            success = uow.ingredientes.delete(id)
            if success:
                uow.commit()
            return success
