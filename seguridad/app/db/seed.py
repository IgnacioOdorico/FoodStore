"""
Script de seed — carga usuarios iniciales para pruebas.
Idempotente: se puede ejecutar múltiples veces sin duplicar datos.

Uso:
    python -m app.db.seed

Requiere PostgreSQL corriendo con las variables de .env configuradas.

Crea:
  - admin / Admin1234!  (role=admin)
  - juan / Juan1234!    (role=user)
"""

from sqlmodel import Session, select
from app.core.database import engine, create_all_tables
from app.core.security import hash_password
from app.modules.usuarios.model import Usuario


USUARIOS_INICIALES = [
    {
        "username":  "admin",
        "full_name": "Administrador del Sistema",
        "email":     "admin@example.com",
        "password":  "Admin1234!",
        "role":      "admin",
    },
    {
        "username":  "juan",
        "full_name": "Juan Pérez",
        "email":     "juan@example.com",
        "password":  "Juan1234!",
        "role":      "user",
    },
]


def run() -> None:
    print("=== Seed — Seguridad JWT (PostgreSQL) ===")
    create_all_tables()

    with Session(engine) as session:
        for data in USUARIOS_INICIALES:
            existing = session.exec(
                select(Usuario).where(Usuario.username == data["username"])
            ).first()

            if existing:
                print(f"  [=] Ya existe: {data['username']} ({data['role']})")
            else:
                usuario = Usuario(
                    username        = data["username"],
                    full_name       = data["full_name"],
                    email           = data["email"],
                    hashed_password = hash_password(data["password"]),
                    role            = data["role"],
                )
                session.add(usuario)
                print(f"  [+] Creado:    {data['username']} / {data['password']}  (role={data['role']})")

        session.commit()

    print("\nUsuarios disponibles para pruebas:")
    print("  admin / Admin1234!  → role=admin  (acceso total)")
    print("  juan  / Juan1234!   → role=user   (acceso básico)")
    print()


if __name__ == "__main__":
    run()
