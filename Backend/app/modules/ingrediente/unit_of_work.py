from app.core.unit_of_work import UnitOfWork
from app.modules.ingrediente.repository import IngredienteRepository

class IngredienteUnitOfWork(UnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.ingredientes = IngredienteRepository(self.session)
        return self
