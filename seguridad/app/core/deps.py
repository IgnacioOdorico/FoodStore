"""
Dependencias de autenticación y autorización para FastAPI.

Este módulo define funciones que se inyectan con Depends() para:
- Extraer el token JWT desde el request
- Validar autenticación
- Validar estado del usuario
- Validar permisos (roles)

Flujo de ejecución típico:

    Request HTTP
        ↓
    oauth2_scheme → extrae el token Bearer del header Authorization
        ↓
    get_current_user → decodifica el JWT y busca el usuario en DB
        ↓
    get_current_active_user → valida que el usuario esté activo
        ↓
    require_role([...]) → valida permisos (RBAC)

Convenciones HTTP:
    401 → No autenticado (token inválido, ausente o expirado)
    403 → Autenticado pero sin permisos suficientes

Arquitectura:
    - Capa Core (dependencias reutilizables)
    - Depende de:
        * Unit of Work (acceso a datos)
        * Seguridad (JWT)
        * Modelo Usuario
"""

from typing import Annotated  # Permite tipado enriquecido para Depends

from fastapi import Depends, HTTPException, status  # Inyección y manejo de errores HTTP
from fastapi.security import OAuth2PasswordBearer  # Manejo estándar de OAuth2 con Bearer

from app.core.security import decode_access_token  # Función para decodificar JWT
from app.core.uow import UnitOfWork, get_uow       # Patrón Unit of Work para DB
from app.modules.usuarios.model import Usuario     # Modelo de dominio Usuario
from app.modules.usuarios.model import UserPublic     # Modelo de dominio Usuario

from fastapi import Request

class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        # 1. Obtener el token EXCLUSIVAMENTE de la cookie (HttpOnly)
        token = request.cookies.get("access_token")
        
        # 2. El soporte para el header Authorization fue deshabilitado.
        # ¿Por qué? Para maximizar la seguridad y forzar el uso de cookies HttpOnly.
        # Las cookies HttpOnly no pueden ser leídas por JavaScript (mitigando ataques XSS).
        # Si permitiéramos usar el token vía header, el frontend tendría que manipular
        # el token en texto plano, arruinando el propósito de la cookie HttpOnly.
        # 
        # if not token:
        #     authorization = request.headers.get("Authorization")
        #     if authorization and authorization.startswith("Bearer "):
        #         token = authorization.split(" ")[1]
                
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No autenticado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return token

# Define el esquema OAuth2 que extrae el token de la cookie (o header)
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/token")



async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],  # Token extraído automáticamente
    uow: Annotated[UnitOfWork, Depends(get_uow)],   # Inyección del Unit of Work
):
    """
    Decodifica el JWT y retorna el Usuario correspondiente.

    Responsabilidades:
    - Validar token
    - Extraer identidad (username)
    - Buscar usuario en base de datos
    """

    # Excepción estándar para errores de autenticación (401)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},  # Obligatorio en OAuth2 por protocolo
    )

    # Decodifica el JWT → devuelve payload o None si es inválido
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extrae el "subject" (usuario) del token
    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception

    # Abre contexto de Unit of Work (manejo de sesión/transacción)
    with uow:
        # Busca el usuario en base de datos
        user = uow.usuarios.get_by_username(username)

        # Si no existe el usuario → token inválido
        if user is None:
            raise credentials_exception

        return UserPublic.model_validate(user)  # Usuario autenticado válido


async def get_current_active_user(
    current_user: Annotated[Usuario, Depends(get_current_user)],
) :
    """
    Verifica que el usuario autenticado esté activo.

    Regla de negocio:
    - Un usuario con disabled=True no puede operar
    """

    if current_user.disabled:
        # Error semántico: el usuario existe pero no puede operar
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario desactivada",
        )

    return UserPublic.model_validate(current_user) # Usuario válido y activo


def require_role(allowed_roles: list[str]):
    """
    Factory de dependencias para control de acceso basado en roles (RBAC).

    Genera dinámicamente una dependencia que valida si el usuario
    tiene uno de los roles permitidos.

    Parámetros:
        allowed_roles → lista de roles válidos (ej: ["admin", "manager"])

    Uso típico:
        @router.get("/admin", dependencies=[Depends(require_role(["admin"]))])
    """

    async def role_checker(
        current_user: Annotated[Usuario, Depends(get_current_active_user)],
    ) -> Usuario:
        """
        Valida que el rol del usuario esté dentro de los permitidos.
        """

        # Si el rol del usuario no está permitido → 403 (prohibido)
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permisos insuficientes. Tu rol es '{current_user.role}'. "
                    f"Se requiere uno de: {allowed_roles}"
                ),
            )

        return current_user  # Usuario autorizado

    return role_checker  # Retorna la dependencia configurada