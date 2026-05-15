from sqlmodel import SQLModel, Field
from datetime import datetime

class ProductoCategoria(SQLModel, table=True):
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)
    es_principal: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)

class ProductoIngrediente(SQLModel, table=True):
    __tablename__ = "producto_ingrediente"
    producto_id:    int   = Field(foreign_key="producto.id", primary_key=True)
    ingrediente_id: int   = Field(foreign_key="ingrediente.id", primary_key=True)
    cantidad:       float = Field(default=0.0) # Cantidad del ingrediente necesaria para el producto
    es_removible:   bool  = Field(default=False)
