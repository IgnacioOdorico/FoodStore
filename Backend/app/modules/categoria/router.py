from typing import List, Annotated, Optional
from fastapi import APIRouter, HTTPException, Query
from app.modules.categoria.service import CategoriaService
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead, CategoriaReadWithChildren

router = APIRouter(prefix="/categorias", tags=["Categorias"])
service = CategoriaService()

@router.get("/", response_model=List[CategoriaRead])
def list_categorias(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    parent_only: Annotated[bool, Query(description="Solo categorías raíz")] = False
):
    """
    Lista las categorías. Permite filtrar por nombre o mostrar solo las raíz.
    """
    return service.list_categorias(nombre=nombre, parent_only=parent_only)

@router.post("/", response_model=CategoriaRead)
def create_categoria(data: CategoriaCreate):
    return service.create_categoria(data)

@router.get("/{id}", response_model=CategoriaRead)
def get_categoria(id: int):
    categoria = service.get_categoria(id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.put("/{id}", response_model=CategoriaRead)
def update_categoria(id: int, data: CategoriaUpdate):
    categoria = service.update_categoria(id, data)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.delete("/{id}")
def delete_categoria(id: int):
    success = service.delete_categoria(id)
    if not success:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return {"message": "Categoria eliminada"}
