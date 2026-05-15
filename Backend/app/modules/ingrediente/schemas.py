from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class IngredienteBase(BaseModel):
    nombre: str
    unidad_medida: str
    stock_minimo: float = 0.0
    es_alergeno: bool = False

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock_minimo: Optional[float] = None
    es_alergeno: Optional[bool] = None

class IngredienteRead(IngredienteBase):
    id: int
    stock_actual: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
