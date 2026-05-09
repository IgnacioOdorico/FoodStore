"""
Repositorio de Producto.

Acceso a BD: queries sin lógica de negocio.
Hereda de BaseRepository[Producto] y agrega queries específicas.

Capa: Repository
Conoce a: Model (Producto), Session
NO conoce a: Service, Router
"""

from sqlmodel import Session

from app.core.base_repository import BaseRepository
from app.modules.producto.models import Producto


class ProductoRepository(BaseRepository[Producto]):

    def __init__(self, session: Session):
        super().__init__(Producto, session)
