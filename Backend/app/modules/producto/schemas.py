from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    imagenes_url: List[str] = []
    stock_cantidad: int = 0
    disponible: bool = True

class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = Field(..., min_length=1, description="Debe pertenecer a al menos una categoría")
    ingrediente_ids: List[int] = []

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = None
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = Field(None, min_length=1)
    ingrediente_ids: Optional[List[int]] = None

class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Schemas para las relaciones N:N con datos extra
from app.modules.categoria.schemas import CategoriaRead
from app.modules.ingrediente.schemas import IngredienteRead

class CategoriaConExtra(CategoriaRead):
    es_principal: bool = False

class IngredienteConExtra(IngredienteRead):
    es_removible: bool = False

class ProductoReadWithDetails(ProductoRead):
    categorias: List[CategoriaConExtra] = []
    ingredientes: List[IngredienteConExtra] = []
