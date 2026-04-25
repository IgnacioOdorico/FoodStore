from sqlmodel import select
from typing import List
from app.modules.categoria.unit_of_work import CategoriaUnitOfWork
from app.modules.categoria.models import Categoria
from app.modules.categoria.schemas import CategoriaCreate, CategoriaUpdate, CategoriaRead

class CategoriaService:
    def list_categorias(self, nombre: str = None, parent_only: bool = False):
        with CategoriaUnitOfWork() as uow:
            statement = select(Categoria).where(Categoria.deleted_at == None)
            if nombre:
                statement = statement.where(Categoria.nombre.contains(nombre))
            if parent_only:
                statement = statement.where(Categoria.parent_id == None)
            
            items = uow.session.exec(statement).all()
            return [CategoriaRead.model_validate(i) for i in items]

    def create_categoria(self, data: CategoriaCreate):
        with CategoriaUnitOfWork() as uow:
            categoria = Categoria(**data.model_dump())
            uow.categorias.create(categoria)
            uow.commit()
            uow.session.refresh(categoria)
            return CategoriaRead.model_validate(categoria)

    def get_categoria(self, id: int):
        with CategoriaUnitOfWork() as uow:
            categoria = uow.categorias.get(id)
            return CategoriaRead.model_validate(categoria) if categoria else None

    def update_categoria(self, id: int, data: CategoriaUpdate):
        with CategoriaUnitOfWork() as uow:
            categoria = uow.categorias.get(id)
            if not categoria:
                return None
            
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(categoria, key, value)
            
            uow.categorias.update(categoria)
            uow.commit()
            uow.session.refresh(categoria)
            return CategoriaRead.model_validate(categoria)

    def delete_categoria(self, id: int):
        with CategoriaUnitOfWork() as uow:
            # 1. Obtener todos los descendientes (incluyendo el ID actual)
            all_ids = self.get_descendant_ids(id)
            
            # 2. Borrar categorías (soft delete)
            from datetime import datetime
            now = datetime.now()
            
            for cid in all_ids:
                cat = uow.session.get(Categoria, cid)
                if cat:
                    cat.deleted_at = now
                    uow.session.add(cat)
            
            # 3. Borrar productos asociados a estas categorías (soft delete)
            # Importamos dentro para evitar líos circulares
            from app.modules.producto.models import Producto, ProductoCategoria
            
            # Buscamos productos que tengan alguna relación con las categorías a borrar
            statement = select(Producto).join(ProductoCategoria).where(
                ProductoCategoria.categoria_id.in_(all_ids),
                Producto.deleted_at == None
            )
            products_to_delete = uow.session.exec(statement).all()
            
            for prod in products_to_delete:
                prod.deleted_at = now
                uow.session.add(prod)
            
            uow.commit()
            return True

    def get_descendant_ids(self, category_id: int) -> List[int]:
        with CategoriaUnitOfWork() as uow:
            # Buscamos recursivamente todos los hijos
            all_ids = [category_id]
            to_process = [category_id]
            while to_process:
                curr_id = to_process.pop()
                # Buscamos hijos directos de este ID
                statement = select(Categoria).where(Categoria.parent_id == curr_id, Categoria.deleted_at == None)
                children = uow.session.exec(statement).all()
                for child in children:
                    if child.id not in all_ids:
                        all_ids.append(child.id)
                        to_process.append(child.id)
            return all_ids

    def get_ancestors(self, category_id: int) -> List[Categoria]:
        with CategoriaUnitOfWork() as uow:
            ancestors = []
            current_id = category_id
            visited = set()
            max_depth = 10 # Seguridad total: ninguna jerarquía debería tener más de 10 niveles
            
            while current_id and current_id not in visited and len(visited) < max_depth:
                visited.add(current_id)
                cat = uow.session.get(Categoria, current_id)
                if not cat or cat.deleted_at:
                    break
                
                if cat.parent_id:
                    parent = uow.session.get(Categoria, cat.parent_id)
                    if parent and not parent.deleted_at:
                        # Si el padre ya está en el árbol, cortamos para evitar rulos
                        if parent.id in visited:
                            break
                        ancestors.append(parent)
                        current_id = parent.id
                    else:
                        break
                else:
                    break
            return ancestors
