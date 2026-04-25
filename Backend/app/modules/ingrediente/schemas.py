from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class IngredienteBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    es_alergeno: bool = False

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    es_alergeno: Optional[bool] = None

class IngredienteRead(IngredienteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
