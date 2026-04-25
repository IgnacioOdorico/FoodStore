from app.core.unit_of_work import UnitOfWork
from app.modules.categoria.repository import CategoriaRepository

class CategoriaUnitOfWork(UnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.categorias = CategoriaRepository(self.session)
        return self
