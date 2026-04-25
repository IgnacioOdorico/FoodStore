from app.core.repository import BaseRepository
from app.modules.ingrediente.models import Ingrediente
from sqlmodel import Session

class IngredienteRepository(BaseRepository[Ingrediente]):
    def __init__(self, session: Session):
        super().__init__(Ingrediente, session)
