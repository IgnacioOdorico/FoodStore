from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None

class CategoriaRead(CategoriaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CategoriaReadWithChildren(CategoriaRead):
    children: List[CategoriaRead] = []
