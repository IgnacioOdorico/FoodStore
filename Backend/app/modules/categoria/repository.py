"""
Repositorio de Categoria.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Categoria] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Categoria), Session
NO conoce a: Service, Router
"""

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.categoria.models import Categoria


class CategoriaRepository(BaseRepository[Categoria]):

    def __init__(self, session: Session):
        super().__init__(Categoria, session)

    def get_by_nombre(self, nombre: str) -> Categoria | None:
        return self.session.exec(
            select(Categoria).where(
                Categoria.nombre == nombre,
                Categoria.deleted_at == None,  # noqa: E711
            )
        ).first()

    def exists_nombre_excluding(self, nombre: str, exclude_id: int) -> bool:
        result = self.session.exec(
            select(Categoria).where(
                Categoria.nombre == nombre,
                Categoria.id != exclude_id,
                Categoria.deleted_at == None,  # noqa: E711
            )
        ).first()
        return result is not None
