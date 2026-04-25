from app.core.unit_of_work import UnitOfWork
from app.modules.producto.repository import ProductoRepository

class ProductoUnitOfWork(UnitOfWork):
    def __enter__(self):
        super().__enter__()
        self.productos = ProductoRepository(self.session)
        return self
