"""
Repositorio de Usuario.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Usuario] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Usuario), Session
NO conoce a: Service, Router
"""

from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.usuarios.model import Usuario


class UsuarioRepository(BaseRepository[Usuario]):

    def __init__(self, session: Session):
        super().__init__(Usuario, session)

    def get_by_username(self, username: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

    def get_by_email(self, email: str) -> Usuario | None:
        return self.session.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()
