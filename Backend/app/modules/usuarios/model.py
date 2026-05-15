"""
Modelos del Dominio 1: Identidad & Acceso.

Cumple con las especificaciones del food_store_erd_v5.svg:
  - Usuario: Datos personales y auditoría.
  - Rol: Catálogo de roles con PK semántica.
  - UsuarioRol: Tabla intermedia con atributos adicionales (RBAC).
  - RefreshToken: Gestión de sesiones y rotación de tokens.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.modules.pedidos.models import Pedido

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UsuarioRol(SQLModel, table=True):
    """
    Tabla de vinculación N:N entre Usuario y Rol.
    Incluye metadatos sobre quién asignó el rol y cuándo expira.
    """
    __tablename__ = "usuario_rol"

    usuario_id:      int       = Field(foreign_key="usuario.id", primary_key=True)
    rol_codigo:      str       = Field(foreign_key="rol.codigo", primary_key=True, max_length=20)
    
    asignado_por_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    expires_at:      Optional[datetime] = Field(default=None)
    created_at:      datetime  = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relaciones
    usuario: "Usuario" = Relationship(
        back_populates="roles_link",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.usuario_id]"}
    )
    rol:     "Rol"     = Relationship(back_populates="usuarios_link")


class Rol(SQLModel, table=True):
    """
    Catálogo de roles (ADMIN, STOCK, PEDIDOS, CLIENT).
    Usa PK semántica (el código es la PK).
    """
    __tablename__ = "rol"

    codigo:      str  = Field(primary_key=True, max_length=20)
    nombre:      str  = Field(unique=True, index=True, nullable=False, max_length=50)
    descripcion: Optional[str] = Field(default=None)

    # Relación N:N vía UsuarioRol
    usuarios_link: List[UsuarioRol] = Relationship(back_populates="rol")


class RefreshToken(SQLModel, table=True):
    """
    Persistencia de Refresh Tokens para rotación de sesiones.
    Sigue el patrón del ERD v5 (token_hash SHA-256).
    """
    __tablename__ = "refresh_token"

    id:          Optional[int] = Field(default=None, primary_key=True)
    usuario_id:  int           = Field(foreign_key="usuario.id", nullable=False)
    token_hash:  str           = Field(unique=True, index=True, nullable=False, max_length=64)
    expires_at:  datetime      = Field(nullable=False)
    revoked_at:  Optional[datetime] = Field(default=None)
    created_at:  datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="refresh_tokens")


class Usuario(SQLModel, table=True):
    """
    Entidad principal de Usuario.
    No incluye 'username' ya que el 'email' es el identificador único según UML.
    """
    __tablename__ = "usuario"

    id:            Optional[int] = Field(default=None, primary_key=True)
    nombre:        str           = Field(max_length=80, nullable=False)
    apellido:      str           = Field(max_length=80, nullable=False)
    email:         str           = Field(unique=True, index=True, nullable=False, max_length=254)
    celular:       Optional[str] = Field(default=None, max_length=20)
    password_hash: str           = Field(max_length=60, nullable=False) # Bcrypt hash
    
    # Audit
    created_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at:    datetime      = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at:    Optional[datetime] = Field(default=None)

    # Relaciones
    roles_link:     List[UsuarioRol] = Relationship(
        back_populates="usuario",
        sa_relationship_kwargs={"foreign_keys": "[UsuarioRol.usuario_id]"}
    )
    refresh_tokens: List[RefreshToken] = Relationship(back_populates="usuario")
    pedidos:        List["Pedido"] = Relationship(back_populates="usuario")


# ─── Esquemas de Intercambio (Schemas / DTOs) ────────────────────────────────

class UserCreate(SQLModel):
    """Esquema para registro de nuevos usuarios."""
    nombre:   str
    apellido: str
    email:    EmailStr
    celular:  Optional[str] = None
    password: str = Field(min_length=8)


class UserPublic(SQLModel):
    """Esquema de respuesta segura (excluye datos sensibles)."""
    id:         int
    nombre:     str
    apellido:   str
    email:      str
    celular:    Optional[str]
    roles:      List[str] = [] # Lista de códigos de roles (ej: ["ADMIN"])
    created_at: datetime


class Token(SQLModel):
    """Respuesta estándar de autenticación."""
    access_token:  str
    refresh_token: Optional[str] = None
    token_type:    str = "bearer"
    expires_in:    int
