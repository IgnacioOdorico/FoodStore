from sqlmodel import select, text
from app.modules.producto.unit_of_work import ProductoUnitOfWork
from app.modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente
from app.modules.producto.schemas import (
    ProductoCreate, 
    ProductoUpdate, 
    ProductoReadWithDetails
)

class ProductoService:
    def list_productos(self, nombre: str = None, disponible: bool = None, categoria_id: int = None):
        # USO EL UNIT OF WORK: Esto me asegura que la sesión se abra y se cierre sola.
        # Es mucho más prolijo que andar pasando la DB por parámetro a todos lados.
        with ProductoUnitOfWork() as uow:
            # Solo traigo los que NO están borrados (Soft Delete)
            statement = select(Producto).where(Producto.deleted_at == None)
            
            # Filtros dinámicos: Si el usuario manda nombre, filtro. Si no, no.
            if nombre:
                statement = statement.where(Producto.nombre.contains(nombre))
            if disponible is not None:
                statement = statement.where(Producto.disponible == disponible)
            
            # Búsqueda jerárquica: Si filtro por una categoría padre, quiero ver los productos de las hijas también.
            if categoria_id:
                from app.modules.categoria.service import CategoriaService
                cat_service = CategoriaService()
                relevant_ids = cat_service.get_descendant_ids(categoria_id)
                statement = statement.join(ProductoCategoria).where(ProductoCategoria.categoria_id.in_(relevant_ids))
                statement = statement.distinct()
            
            items = uow.session.exec(statement).all()
            # Cargo las relaciones manualmente para que no me den error de 'Lazy Loading' fuera de la sesión.
            for i in items:
                _ = i.categorias
                _ = i.ingredientes
            return [ProductoReadWithDetails.model_validate(i) for i in items]

    def create_producto(self, data: ProductoCreate):
        with ProductoUnitOfWork() as uow:
            # Separo los IDs de relaciones de la data del producto para guardarlos por separado.
            categoria_ids = data.categoria_ids
            ingrediente_ids = data.ingrediente_ids
            prod_data = data.model_dump(exclude={"categoria_ids", "ingrediente_ids"})
            
            producto = Producto(**prod_data)
            uow.productos.create(producto)
            uow.commit() # Guardo el producto primero para tener el ID
            uow.session.refresh(producto)

            # Ahora guardo las relaciones en las tablas intermedias (N:N)
            for cat_id in categoria_ids:
                uow.session.add(ProductoCategoria(producto_id=producto.id, categoria_id=cat_id, es_principal=True))
            for ing_id in ingrediente_ids:
                uow.session.add(ProductoIngrediente(producto_id=producto.id, ingrediente_id=ing_id))
            
            uow.commit() # Si algo falla acá, el rollback del UOW me protege.
            uow.session.refresh(producto)
            return self.get_producto(producto.id)

    def get_producto(self, id: int):
        with ProductoUnitOfWork() as uow:
            producto = uow.productos.get(id)
            if not producto:
                return None
            
            # Expire me sirve para forzar a SQLAlchemy a que vuelva a leer las relaciones de la DB
            # Esto evita que me devuelva datos viejos que están en la caché de la sesión.
            uow.session.expire(producto, ["categorias", "ingredientes"])
            dto = ProductoReadWithDetails.model_validate(producto)
            
            # Acá "relleno" los datos extras de la relación (como es_principal o es_removible)
            # que no vienen directamente en el objeto de SQLAlchemy.
            for cat_dto in dto.categorias:
                link = uow.session.exec(
                    select(ProductoCategoria).where(
                        ProductoCategoria.producto_id == id,
                        ProductoCategoria.categoria_id == cat_dto.id
                    )
                ).first()
                if link:
                    cat_dto.es_principal = link.es_principal

            for ing_dto in dto.ingredientes:
                link = uow.session.exec(
                    select(ProductoIngrediente).where(
                        ProductoIngrediente.producto_id == id,
                        ProductoIngrediente.ingrediente_id == ing_dto.id
                    )
                ).first()
                if link:
                    ing_dto.es_removible = link.es_removible

            return dto

    def delete_producto(self, id: int):
        with ProductoUnitOfWork() as uow:
            # Uso el repositorio para borrar. El repo ya sabe que tiene que hacer un 'Soft Delete'.
            success = uow.productos.delete(id)
            if success:
                uow.commit()
            return success
