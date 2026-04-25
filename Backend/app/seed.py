from sqlmodel import Session, SQLModel, text
from app.core.database import engine
from app.modules.producto.models import Producto, ProductoCategoria, ProductoIngrediente
from app.modules.categoria.models import Categoria
from app.modules.ingrediente.models import Ingrediente

def seed_data():
    with Session(engine) as session:
        print("Limpiando base de datos (incluyendo tablas legacy)...")
        # SQLModel drop_all 
        session.execute(text("DROP TABLE IF EXISTS detallepedido CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS pedido CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS productocategoria CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS productoingrediente CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS producto CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS categoria CASCADE"))
        session.execute(text("DROP TABLE IF EXISTS ingrediente CASCADE"))
        session.commit()
        
        print("Creando tablas con el nuevo esquema...")
        SQLModel.metadata.create_all(engine)
        
        print("Iniciando siembra de datos...")

        # 1. Crear Categorías Jerárquicas
        cat_comida = Categoria(nombre="Comida", descripcion="Todo tipo de platos")
        session.add(cat_comida)
        session.commit()
        session.refresh(cat_comida)

        cat_pizzas = Categoria(nombre="Pizzas", descripcion="Pizzas artesanales", parent_id=cat_comida.id)
        cat_bebidas = Categoria(nombre="Bebidas", descripcion="Refrescos y cervezas")
        
        session.add(cat_pizzas)
        session.add(cat_bebidas)
        session.commit()
        session.refresh(cat_pizzas)
        session.refresh(cat_bebidas)

        # 2. Crear Ingredientes
        ing_queso = Ingrediente(nombre="Queso Muzzarella", descripcion="Queso de alta calidad", es_alergeno=True)
        ing_tomate = Ingrediente(nombre="Salsa de Tomate", descripcion="Tomates frescos triturados")
        
        session.add(ing_queso)
        session.add(ing_tomate)
        session.commit()
        session.refresh(ing_queso)
        session.refresh(ing_tomate)

        # 3. Crear Productos
        p1 = Producto(
            nombre="Muzzarella Especial", 
            descripcion="Mucha muzzarella y aceitunas", 
            precio_base=8500.0,
            imagenes_url=["https://images.unsplash.com/photo-1513104890138-7c749659a591"],
            stock_cantidad=20,
            disponible=True
        )
        session.add(p1)
        session.commit()
        session.refresh(p1)

        # 4. Relaciones N:N
        rel_cat = ProductoCategoria(producto_id=p1.id, categoria_id=cat_pizzas.id, es_principal=True)
        rel_ing1 = ProductoIngrediente(producto_id=p1.id, ingrediente_id=ing_queso.id, es_removible=False)
        rel_ing2 = ProductoIngrediente(producto_id=p1.id, ingrediente_id=ing_tomate.id, es_removible=True)
        
        session.add(rel_cat)
        session.add(rel_ing1)
        session.add(rel_ing2)
        session.commit()

        print("Datos sembrados con exito.")

if __name__ == "__main__":
    seed_data()
