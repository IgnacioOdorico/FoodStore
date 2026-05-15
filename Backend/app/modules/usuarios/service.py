"""
Service de Usuario — lógica de negocio.

Orquesta operaciones sobre los repositorios a través del UoW.
Implementa registro, autenticación y gestión de roles según ERD v5.
"""

from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import Usuario, UserCreate, Token, UserPublic, UsuarioRol


class UsuarioService:
    """Lógica de negocio para autenticación y gestión de usuarios."""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def register(self, user_in: UserCreate) -> UserPublic:
        """Registra un nuevo usuario con el rol 'CLIENT' por defecto."""
        
        if self.uow.usuarios.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado",
            )

        # 1. Crear el usuario
        usuario = Usuario(
            nombre=user_in.nombre,
            apellido=user_in.apellido,
            email=user_in.email,
            celular=user_in.celular,
            password_hash=hash_password(user_in.password),
        )

        user_db = self.uow.usuarios.add(usuario)
        self.uow.commit() # Asegura ID para la tabla intermedia

        # 2. Asignar rol CLIENT por defecto (requiere seed de roles)
        rol_client = self.uow.roles.get_by_codigo("CLIENT")
        if not rol_client:
            # Fallback por si no se corrió el seed (no recomendado en prod)
            from app.modules.usuarios.model import Rol
            rol_client = self.uow.roles.add(Rol(codigo="CLIENT", nombre="Cliente"))
            self.uow.commit()

        self.uow.usuarios_roles.add(UsuarioRol(
            usuario_id=user_db.id,
            rol_codigo="CLIENT"
        ))

        # 3. Retornar vista pública con roles
        return self._to_public(user_db)

    def authenticate(self, email: str, password: str) -> Token:
        """Autentica con email + password y retorna un Token con JWT."""
        
        user = self.uow.usuarios.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if user.deleted_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cuenta de usuario eliminada",
            )

        # Obtener códigos de roles para el payload del JWT
        roles = self.uow.usuarios.get_roles_codes(user.id)

        access_token = create_access_token(
            data={
                "sub": user.email, 
                "roles": roles,
                "name": f"{user.nombre} {user.apellido}"
            }
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    def list_all(self) -> List[UserPublic]:
        """Lista todos los usuarios activos."""
        usuarios = self.uow.usuarios.get_all()
        return [self._to_public(u) for u in usuarios if not u.deleted_at]

    def delete_user(self, user_id: int) -> UserPublic:
        """Realiza un soft-delete del usuario."""
        user = self.uow.usuarios.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
        user.deleted_at = datetime.now(timezone.utc)
        updated = self.uow.usuarios.update(user)
        return self._to_public(updated)

    def _to_public(self, user: Usuario) -> UserPublic:
        """Helper para convertir Modelo a Schema con roles cargados."""
        roles = self.uow.usuarios.get_roles_codes(user.id)
        return UserPublic(
            id=user.id,
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email,
            celular=user.celular,
            roles=roles,
            created_at=user.created_at
        )
