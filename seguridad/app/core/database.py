"""
Engine SQLModel y factory de sesión.

Usa PostgreSQL (igual que u_05_v2) configurado vía variables de entorno.
Los tests sobreescriben get_session con SQLite en memoria — sin tocar este módulo.
"""

from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# PostgreSQL no necesita connect_args especiales.
# check_same_thread=False era exclusivo de SQLite; aquí ya no aplica.
engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session():
    """Dependencia FastAPI: provee una sesión de BD por request."""
    with Session(engine) as session:
        yield session


def create_all_tables() -> None:
    """Crea las tablas registradas en SQLModel.metadata al arrancar la app."""
    import app.modules.usuarios.model     # noqa: F401 — registra el modelo en metadata
    import app.modules.categorias.model   # noqa: F401
    SQLModel.metadata.create_all(engine)
