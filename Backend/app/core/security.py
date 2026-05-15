"""
Utilidades de seguridad centralizadas.

Responsabilidades:
- Hashing de contraseñas usando bcrypt (a través de passlib)
- Generación y validación de JWT (firma HS256 con python-jose)

Motivación:
- Evitar duplicación de lógica de seguridad
- Permitir reutilización (routers, seeds, tests, etc.)
- Mantener separación de capas (no mezclar con endpoints)
"""

# Manejo de fechas para expiración de tokens (timezone-aware → correcto)
from datetime import datetime, timedelta, timezone

# Librería para JWT (encode/decode + manejo de errores)
from jose import JWTError, jwt


# Configuración central (SECRET_KEY, ALGORITHM, expiración, etc.)
from app.core.config import settings


# ─────────────────────────────────────────────────────────────────────────────
# HASHING DE CONTRASEÑAS (bcrypt)
# ─────────────────────────────────────────────────────────────────────────────

import bcrypt


def hash_password(plain: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve su hash bcrypt.
    Se usa la librería bcrypt directamente para evitar incompatibilidades con passlib.
    """
    pwd_bytes = plain.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash bcrypt.
    """
    pwd_bytes = plain.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


# ─────────────────────────────────────────────────────────────────────────────
# JWT (JSON Web Tokens)
# ─────────────────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Genera un JWT firmado (HS256).

    Parámetros:
    - data: payload base (ej: {"sub": username, "role": role})
    - expires_delta: override opcional del tiempo de expiración

    Comportamiento:
    - Clona el payload (evita mutación externa)
    - Calcula expiración 
    - Agrega claims estándar:
        * "exp"  → expiración
        * "type" → tipo de token (acceso)

    Retorna:
    - Token JWT firmado (string)
    """

    # Copia defensiva del payload
    to_encode = data.copy()

    # Define expiración:
    # - usa valor custom si viene
    # - sino usa config global
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Agrega claims al payload
    to_encode.update({
        "type": "access",  # distingue access vs refresh (buena práctica)
        "exp": expire      # claim estándar JWT
    })

    # Firma el token:
    # - SECRET_KEY → clave simétrica
    # - ALGORITHM → HS256
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT.

    Validaciones implícitas de jwt.decode():
    - Firma válida
    - Algoritmo permitido
    - Expiración (exp)

    Validación adicional:
    - "type" == "access" (evita usar refresh token como access)

    Retorna:
    - dict → payload válido
    - None → token inválido (cualquier error)

    Nota de diseño:
    - Se encapsulan excepciones → el caller no maneja errores criptográficos
    """

    try:
        # Decodifica y valida firma + exp
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Validación de tipo de token (defensa extra)
        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        # Cualquier problema (firma, expiración, formato, etc.)
        return None