"""
Script de seed completo — FoodStore (ERD v5).

Carga:
  1. Roles (ADMIN, STOCK, PEDIDOS, CLIENT)
  2. Usuarios (Nacho Admin, Juan Cliente)
  3. Categorías (Pizzas, Bebidas, Hamburguesas)
  4. Ingredientes (Harina, Tomate, Muzarella, Carne, Lechuga, Coca-Cola)
  5. Productos (Muzarella, Hamburguesa, Coca) + Asociaciones (Categorías e Ingredientes)
  6. Pedidos (Un pedido de prueba para Juan)

Uso:
    python -m app.db.seed
"""

from datetime import datetime, timezone
from sqlmodel import Session, select
from app.core.database import engine, create_all_tables
from app.core.security import hash_password

# Imports de Modelos
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol
from app.modules.categorias.model import Categoria
from app.modules.ingrediente.models import Ingrediente
from app.modules.producto.models import Producto
from app.modules.producto.associations import ProductoCategoria, ProductoIngrediente
from app.modules.pedidos.models import Pedido, DetallePedido


def run() -> None:
    print("🚀 Iniciando Sembrado de Datos (FoodStore ERD v5)...")
    create_all_tables()

    with Session(engine) as session:
        # --- 1. ROLES ---
        roles_data = [
            {"codigo": "ADMIN",   "nombre": "Administrador", "descripcion": "Acceso total"},
            {"codigo": "STOCK",   "nombre": "Gestor de Stock", "descripcion": "Productos e Ingredientes"},
            {"codigo": "PEDIDOS", "nombre": "Gestor de Pedidos", "descripcion": "Ventas y Comandas"},
            {"codigo": "CLIENT",  "nombre": "Cliente", "descripcion": "Usuario final"},
        ]
        roles_db = {}
        for r in roles_data:
            db_rol = session.get(Rol, r["codigo"])
            if not db_rol:
                db_rol = Rol(**r)
                session.add(db_rol)
                print(f"  [+] Rol: {r['codigo']}")
            roles_db[r["codigo"]] = db_rol
        session.commit()

        # --- 2. USUARIOS ---
        usuarios_data = [
            {
                "nombre": "Nacho", "apellido": "Admin", "email": "admin@nachopizza.com",
                "password": "Admin1234!", "roles": ["ADMIN"]
            },
            {
                "nombre": "Juan", "apellido": "Cliente", "email": "juan@ejemplo.com",
                "password": "Juan1234!", "roles": ["CLIENT"]
            },
        ]
        users_db = {}
        for u in usuarios_data:
            db_user = session.exec(select(Usuario).where(Usuario.email == u["email"])).first()
            if not db_user:
                db_user = Usuario(
                    nombre=u["nombre"],
                    apellido=u["apellido"],
                    email=u["email"],
                    password_hash=hash_password(u["password"])
                )
                session.add(db_user)
                session.flush()
                for r_code in u["roles"]:
                    session.add(UsuarioRol(usuario_id=db_user.id, rol_codigo=r_code))
                print(f"  [+] Usuario: {u['email']}")
            users_db[u["email"]] = db_user
        session.commit()

        # --- 3. CATEGORÍAS ---
        cats_data = [
            {"nombre": "Pizzas", "descripcion": "Pizzas a la piedra"},
            {"nombre": "Bebidas", "descripcion": "Gaseosas y Cervezas"},
            {"nombre": "Hamburguesas", "descripcion": "Burgers Gourmet"},
        ]
        cats_db = {}
        for c in cats_data:
            db_cat = session.exec(select(Categoria).where(Categoria.nombre == c["nombre"])).first()
            if not db_cat:
                db_cat = Categoria(**c)
                session.add(db_cat)
                print(f"  [+] Categoría: {c['nombre']}")
            cats_db[c["nombre"]] = db_cat
        session.commit()

        # --- 4. INGREDIENTES ---
        ing_data = [
            {"nombre": "Harina", "unidad_medida": "g", "stock_actual": 5000, "stock_minimo": 1000},
            {"nombre": "Muzarella", "unidad_medida": "g", "stock_actual": 2000, "stock_minimo": 500},
            {"nombre": "Tomate", "unidad_medida": "un", "stock_actual": 50, "stock_minimo": 10},
            {"nombre": "Medallón Carne", "unidad_medida": "un", "stock_actual": 30, "stock_minimo": 5},
            {"nombre": "Coca-Cola 500ml", "unidad_medida": "un", "stock_actual": 24, "stock_minimo": 6},
        ]
        ings_db = {}
        for i in ing_data:
            db_ing = session.exec(select(Ingrediente).where(Ingrediente.nombre == i["nombre"])).first()
            if not db_ing:
                db_ing = Ingrediente(**i)
                session.add(db_ing)
                print(f"  [+] Ingrediente: {i['nombre']}")
            ings_db[i["nombre"]] = db_ing
        session.commit()

        # --- 5. PRODUCTOS ---
        prods_data = [
            {
                "nombre": "Pizza Muzarella", "precio": 8500.0, "cat": "Pizzas",
                "ings": [("Harina", 250), ("Muzarella", 200), ("Tomate", 2)]
            },
            {
                "nombre": "Hamburguesa Clásica", "precio": 6200.0, "cat": "Hamburguesas",
                "ings": [("Medallón Carne", 1), ("Tomate", 1)]
            },
            {
                "nombre": "Coca-Cola", "precio": 1500.0, "cat": "Bebidas",
                "ings": [("Coca-Cola 500ml", 1)]
            },
        ]
        for p in prods_data:
            db_prod = session.exec(select(Producto).where(Producto.nombre == p["nombre"])).first()
            if not db_prod:
                db_prod = Producto(
                    nombre=p["nombre"],
                    descripcion=f"Exquisita {p['nombre']}",
                    precio_base=p["precio"]
                )
                session.add(db_prod)
                session.flush()
                
                # Link Categoría
                cat = cats_db[p["cat"]]
                session.add(ProductoCategoria(producto_id=db_prod.id, categoria_id=cat.id, es_principal=True))
                
                # Link Ingredientes
                for ing_nombre, cant in p["ings"]:
                    ing = ings_db[ing_nombre]
                    session.add(ProductoIngrediente(producto_id=db_prod.id, ingrediente_id=ing.id, cantidad=cant))
                
                print(f"  [+] Producto: {p['nombre']}")
        session.commit()

        # --- 6. PEDIDOS ---
        juan = users_db["juan@ejemplo.com"]
        pizza = session.exec(select(Producto).where(Producto.nombre == "Pizza Muzarella")).first()
        coca = session.exec(select(Producto).where(Producto.nombre == "Coca-Cola")).first()

        if juan and pizza and coca:
            existing_pedido = session.exec(select(Pedido).where(Pedido.usuario_id == juan.id)).first()
            if not existing_pedido:
                nuevo_pedido = Pedido(
                    usuario_id=juan.id,
                    estado="PENDIENTE",
                    metodo_pago="EFECTIVO",
                    total=pizza.precio_base + coca.precio_base
                )
                session.add(nuevo_pedido)
                session.flush()

                # Detalles
                session.add(DetallePedido(
                    pedido_id=nuevo_pedido.id, producto_id=pizza.id, 
                    cantidad=1, precio_unitario=pizza.precio_base, subtotal=pizza.precio_base
                ))
                session.add(DetallePedido(
                    pedido_id=nuevo_pedido.id, producto_id=coca.id, 
                    cantidad=1, precio_unitario=coca.precio_base, subtotal=coca.precio_base
                ))
                print(f"  [+] Pedido de prueba para {juan.email}")

        session.commit()

    print("\n✅ Sembrado finalizado con éxito.")


if __name__ == "__main__":
    run()

