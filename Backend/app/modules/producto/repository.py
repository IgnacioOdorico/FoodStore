from app.core.repository import BaseRepository
from app.modules.producto.models import Producto
from sqlmodel import Session

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(Producto, session)
