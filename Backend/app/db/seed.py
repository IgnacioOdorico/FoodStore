"""
Script de seed — carga roles y usuarios iniciales según ERD v5.
Idempotente: se puede ejecutar múltiples veces sin duplicar datos.

Uso:
    python -m app.db.seed
"""

from sqlmodel import Session, select
from app.core.database import engine, create_all_tables
from app.core.security import hash_password
from app.modules.usuarios.model import Usuario, Rol, UsuarioRol


ROLES_INICIALES = [
    {"codigo": "ADMIN",   "nombre": "Administrador", "descripcion": "Acceso total al sistema"},
    {"codigo": "STOCK",   "nombre": "Gestor de Stock", "descripcion": "Gestión de productos e ingredientes"},
    {"codigo": "PEDIDOS", "nombre": "Gestor de Pedidos", "descripcion": "Gestión de ventas y comandas"},
    {"codigo": "CLIENT",  "nombre": "Cliente", "descripcion": "Usuario final de la app"},
]

USUARIOS_INICIALES = [
    {
        "nombre":   "Nacho",
        "apellido": "Admin",
        "email":    "admin@nachopizza.com",
        "password": "Admin1234!",
        "roles":    ["ADMIN"],
    },
    {
        "nombre":   "Juan",
        "apellido": "Cliente",
        "email":    "juan@ejemplo.com",
        "password": "Juan1234!",
        "roles":    ["CLIENT"],
    },
]


def run() -> None:
    print("=== Seed — FoodStore (ERD v5 Compliance) ===")
    create_all_tables()

    with Session(engine) as session:
        # 1. Cargar Roles
        for r_data in ROLES_INICIALES:
            existing_rol = session.exec(select(Rol).where(Rol.codigo == r_data["codigo"])).first()
            if not existing_rol:
                rol = Rol(**r_data)
                session.add(rol)
                print(f"  [+] Rol creado: {r_data['codigo']}")
        
        session.commit()

        # 2. Cargar Usuarios
        for u_data in USUARIOS_INICIALES:
            existing_user = session.exec(select(Usuario).where(Usuario.email == u_data["email"])).first()
            
            if existing_user:
                print(f"  [=] Usuario ya existe: {u_data['email']}")
                continue

            # Crear Usuario
            usuario = Usuario(
                nombre=u_data["nombre"],
                apellido=u_data["apellido"],
                email=u_data["email"],
                password_hash=hash_password(u_data["password"]),
            )
            session.add(usuario)
            session.flush() # Para obtener el ID del usuario

            # Asignar Roles
            for r_code in u_data["roles"]:
                u_rol = UsuarioRol(usuario_id=usuario.id, rol_codigo=r_code)
                session.add(u_rol)
            
            print(f"  [+] Usuario creado: {u_data['email']} con roles {u_data['roles']}")

        session.commit()

    print("\nSeed finalizado con éxito.")


if __name__ == "__main__":
    run()
