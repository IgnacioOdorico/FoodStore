"""
Engine SQLModel y factory de sesión.

Usa PostgreSQL configurado vía variables de entorno.
Los tests sobreescriben get_session con SQLite en memoria — sin tocar este módulo.
"""

from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def get_session():
    """Dependencia FastAPI: provee una sesión de BD por request."""
    with Session(engine) as session:
        yield session


def create_all_tables() -> None:
    """Crea las tablas registradas en SQLModel.metadata al arrancar la app."""
    import app.modules.usuarios.models          # noqa: F401 — registra el modelo en metadata
    import app.modules.categoria.models         # noqa: F401
    import app.modules.ingrediente.models       # noqa: F401
    import app.modules.producto.models          # noqa: F401
    SQLModel.metadata.create_all(engine)


# Alias de compatibilidad — los servicios que aún usen SessionLocal() siguen funcionando
def SessionLocal():
    return Session(engine)
