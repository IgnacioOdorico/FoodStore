"""
Modelo de Usuario — tabla 'usuario' en PostgreSQL.

Campos clave para seguridad:
  - hashed_password: hash bcrypt (nunca texto plano).
  - role: "user" | "admin" — usado por require_role() para RBAC.
  - disabled: permite desactivar cuentas sin eliminarlas.
"""

from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class Usuario(SQLModel, table=True):
    id:              int | None = Field(default=None, primary_key=True)
    username:        str        = Field(index=True, unique=True)
    full_name:       str
    email:           str        = Field(index=True, unique=True)  
    hashed_password: str
    role:            str        = Field(default="user")           # "user" | "admin"
    disabled:        bool       = Field(default=False)


# ─── Esquemas Pydantic (sin table=True) ──────────────────────────────────────

class UserCreate(SQLModel):
    """Datos requeridos para registrar un usuario."""
    username:  str
    full_name: str
    email:     EmailStr
    password:  str = Field(min_length=8)


class UserPublic(SQLModel):
    """Vista pública del usuario — excluye hashed_password."""
    id:        int
    username:  str
    full_name: str
    email:     str
    role:      str
    disabled:  bool


class Token(SQLModel):
    """Respuesta del endpoint /token."""
    access_token: str
    token_type:   str = "bearer"
    expires_in:   int  # segundos hasta expiración
