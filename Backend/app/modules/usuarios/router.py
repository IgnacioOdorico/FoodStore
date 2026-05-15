"""
Router de autenticación y gestión de usuarios.

Capa: Router
Adaptado al ERD v5.
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.core.uow import UnitOfWork, get_uow
from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.model import UserCreate, UserPublic, Token
from app.modules.usuarios.service import UsuarioService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(
    user_in: UserCreate,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Registra un nuevo usuario."""
    with uow:
        service = UsuarioService(uow)
        return service.register(user_in)


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    response: Response,
):
    """
    Login estándar OAuth2. 
    'username' en el formulario debe ser el email del usuario.
    """
    with uow:
        service = UsuarioService(uow)
        # El formulario de FastAPI usa el campo 'username' para el identificador
        token = service.authenticate(form_data.username, form_data.password)
        
        # Cookie HttpOnly para seguridad (XSS protection)
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            max_age=token.expires_in,
            samesite="lax",
            secure=False, # True en producción con HTTPS
        )
        return {"mensaje": "Login exitoso", "user_email": form_data.username}


@router.post("/logout")
def logout(response: Response):
    """Cierra la sesión eliminando la cookie."""
    response.delete_cookie(key="access_token", httponly=True, samesite="lax")
    return {"mensaje": "Sesión cerrada"}


@router.get("/me", response_model=UserPublic)
def read_me(
    current_user: Annotated[UserPublic, Depends(get_current_active_user)],
):
    """Retorna el perfil del usuario autenticado."""
    return current_user


@router.get("/admin/usuarios", response_model=List[UserPublic])
def list_users(
    _admin: Annotated[UserPublic, Depends(require_role(["ADMIN"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Lista todos los usuarios (Solo ADMIN)."""
    with uow:
        service = UsuarioService(uow)
        return service.list_all()


@router.delete("/admin/usuarios/{user_id}", response_model=UserPublic)
def delete_user(
    user_id: int,
    _admin: Annotated[UserPublic, Depends(require_role(["ADMIN"]))],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Baja lógica de un usuario (Solo ADMIN)."""
    with uow:
        service = UsuarioService(uow)
        return service.delete_user(user_id)
