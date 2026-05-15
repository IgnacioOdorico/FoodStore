from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    imagen_url: Optional[str] = None
    disponible: bool = True

class IngredienteConCantidad(BaseModel):
    id: int
    cantidad: float
    es_removible: bool = False

class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(..., min_length=1)
    ingredientes_receta: List[IngredienteConCantidad] = []

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    imagen_url: Optional[str] = None
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = None
    ingredientes_receta: Optional[List[IngredienteConCantidad]] = None

class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Schemas para las relaciones N:N con datos extra
from app.modules.categorias.model import CategoriaPublic as CategoriaRead
from app.modules.ingrediente.schemas import IngredienteRead

class CategoriaConExtra(CategoriaRead):
    es_principal: bool = False

class IngredienteConExtra(IngredienteRead):
    cantidad: float = 0.0
    es_removible: bool = False

class ProductoReadWithDetails(ProductoRead):
    categorias: List[CategoriaConExtra] = []
    ingredientes: List[IngredienteConExtra] = []
