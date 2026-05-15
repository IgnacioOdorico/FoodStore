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

# Contexto de hashing (abstracción sobre bcrypt)
from passlib.context import CryptContext

# Configuración central (SECRET_KEY, ALGORITHM, expiración, etc.)
from app.core.config import settings


# ─────────────────────────────────────────────────────────────────────────────
# HASHING DE CONTRASEÑAS (bcrypt)
# ─────────────────────────────────────────────────────────────────────────────

# Configura el contexto de hashing:
# - "bcrypt" → algoritmo seguro para contraseñas
# - deprecated="auto" → permite migraciones futuras de algoritmo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve su hash bcrypt.

    Importante:
    - bcrypt incluye salt automáticamente
    - cada hash generado para el mismo input es distinto
    """
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash.

    Internamente:
    - Extrae el salt del hash
    - Recalcula el hash
    - Compara de forma segura (timing-attack safe)
    """
    return pwd_context.verify(plain, hashed)


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