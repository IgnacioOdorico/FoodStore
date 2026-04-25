from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# Importamos los modelos para que SQLModel los registre
from app.modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente
from app.modules.categoria.models import Categoria
from app.modules.ingrediente.models import Ingrediente

from app.core.database import engine

# Importamos los routers refactorizados
from app.modules.categoria.router import router as categoria_router
from app.modules.producto.router import router as producto_router
from app.modules.ingrediente.router import router as ingrediente_router

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Parcial Integrador API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir routers
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
