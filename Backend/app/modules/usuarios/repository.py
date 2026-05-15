"""
Repositorio de Usuario y Roles.

Acceso a BD: queries sin lógica de negocio.
Implementa búsquedas por email y gestión de roles según ERD v5.
"""

from typing import List, Optional
from sqlmodel import Session, select

from app.core.base_repository import BaseRepository
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: Session):
        super().__init__(Usuario, session)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario activo por su email."""
        return self.session.exec(
            select(Usuario).where(
                Usuario.email == email, 
                Usuario.deleted_at == None
            )
        ).first()

    def get_roles_codes(self, usuario_id: int) -> List[str]:
        """Retorna la lista de códigos de roles asignados a un usuario."""
        statement = (
            select(Rol.codigo)
            .join(UsuarioRol)
            .where(UsuarioRol.usuario_id == usuario_id)
        )
        return list(self.session.exec(statement).all())


class RolRepository(BaseRepository[Rol]):
    def __init__(self, session: Session):
        super().__init__(Rol, session)

    def get_by_codigo(self, codigo: str) -> Optional[Rol]:
        return self.session.get(Rol, codigo)


class UsuarioRolRepository(BaseRepository[UsuarioRol]):
    def __init__(self, session: Session):
        super().__init__(UsuarioRol, session)
