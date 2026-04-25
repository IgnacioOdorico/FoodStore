from app.core.repository import BaseRepository
from app.modules.categoria.models import Categoria
from sqlmodel import Session

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(Categoria, session)
