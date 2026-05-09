"""
Repositorio de Ingrediente.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Ingrediente] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Ingrediente), Session
NO conoce a: Service, Router
"""

from sqlmodel import Session

from app.core.base_repository import BaseRepository
from app.modules.ingrediente.models import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):

    def __init__(self, session: Session):
        super().__init__(Ingrediente, session)
