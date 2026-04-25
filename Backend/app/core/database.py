from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import StaticPool

import os
from dotenv import load_dotenv

# Cargamos las variables del .env
load_dotenv()

# DATABASE_URL: Ahora la toma del .env. Si no existe, usa SQLite por las dudas.
database_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# ECHO=TRUE: Esto lo pongo para ver en la consola todas las sentencias SQL que genera el programa.
engine = create_engine(
    database_url, 
    echo=True, 
    # check_same_thread solo se necesita para SQLite
    connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {}
)

# INIT_DB: Esta función crea las tablas si no existen.
def init_db():
    # Importo todos los modelos acá para que SQLModel los registre antes de crear las tablas.
    from app.modules.categoria.models import Categoria
    from app.modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente
    from app.modules.ingrediente.models import Ingrediente
    
    # Crea físicamente el archivo .db y las tablas.
    SQLModel.metadata.create_all(engine)

# SESSIONLOCAL: Es una "fábrica" de sesiones. 
# Cada vez que necesito hablar con la DB, pido una sesión nueva.
def SessionLocal():
    return Session(engine)
