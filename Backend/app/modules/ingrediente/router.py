from typing import List, Annotated, Optional
from fastapi import APIRouter, HTTPException, Query
from app.modules.ingrediente.service import IngredienteService
from app.modules.ingrediente.schemas import IngredienteCreate, IngredienteUpdate, IngredienteRead

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])
service = IngredienteService()

@router.get("/", response_model=List[IngredienteRead])
def list_ingredientes(
    nombre: Annotated[Optional[str], Query(description="Filtrar por nombre")] = None,
    es_alergeno: Annotated[Optional[bool], Query(description="Filtrar por alérgenos")] = None
):
    return service.list_ingredientes(nombre=nombre, es_alergeno=es_alergeno)

@router.post("/", response_model=IngredienteRead)
def create_ingrediente(data: IngredienteCreate):
    return service.create_ingrediente(data)

@router.get("/{id}", response_model=IngredienteRead)
def get_ingrediente(id: int):
    ingrediente = service.get_ingrediente(id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.put("/{id}", response_model=IngredienteRead)
def update_ingrediente(id: int, data: IngredienteUpdate):
    ingrediente = service.update_ingrediente(id, data)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.delete("/{id}")
def delete_ingrediente(id: int):
    success = service.delete_ingrediente(id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return {"message": "Ingrediente eliminado"}
