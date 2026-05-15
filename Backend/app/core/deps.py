"""
Dependencias de autenticación y autorización para FastAPI.

Adaptado al ERD v5:
- Extrae identidad vía 'email' (claim 'sub').
- Valida RBAC contra la lista de roles del usuario.
"""

from typing import Annotated, List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.core.uow import UnitOfWork, get_uow
from app.modules.usuarios.model import Usuario, UserPublic
from app.modules.usuarios.service import UsuarioService


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        token = request.cookies.get("access_token")
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No autenticado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> UserPublic:
    """Decodifica el JWT y retorna la vista pública del Usuario."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    with uow:
        service = UsuarioService(uow)
        user = uow.usuarios.get_by_email(email)
        if user is None:
            raise credentials_exception

        return service._to_public(user)


async def get_current_active_user(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
) -> UserPublic:
    """Verifica que el usuario no esté marcado como eliminado."""
    # En el nuevo modelo, usamos deleted_at. get_current_user ya filtra activos.
    return current_user


def require_role(allowed_roles: List[str]):
    """
    Factory de dependencias para RBAC.
    Valida si al menos uno de los roles del usuario coincide con los permitidos.
    """
    async def role_checker(
        current_user: Annotated[UserPublic, Depends(get_current_active_user)],
    ) -> UserPublic:
        
        # current_user.roles es una List[str] según el nuevo UserPublic
        has_access = any(role in allowed_roles for role in current_user.roles)
        
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {allowed_roles}. Roles actuales: {current_user.roles}",
            )

        return current_user

    return role_checker