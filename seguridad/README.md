# Seguridad JWT — FastAPI

API REST con autenticación JWT, control de acceso por roles (RBAC) y CRUD de categorías.

## Requisitos

- Python 3.11+
- PostgreSQL (local o contenedor)
- pip

## Instalación

```bash
cd seguridad_jwt_pg
pip install -r requirements.txt
```

## Variables de entorno

Crear `.env` en la raíz del proyecto:

```env
# Base de datos (PostgreSQL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=seguridad_jwt_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT — Mínimo 32 caracteres. Cambiar en producción.
SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria_minimo_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Setup Inicial y Precarga de Datos (Seed)

Para probar la API y sus niveles de acceso (RBAC), es necesario inicializar la base de datos PostgreSQL con las tablas requeridas y poblarla con usuarios de prueba.

El proyecto incluye un script de *seed* (semilla) en `app/db/seed.py` que se encarga de todo automáticamente (crea las tablas si no existen y genera los usuarios). Es un proceso **idempotente**, por lo que puedes ejecutarlo varias veces de forma segura sin duplicar registros.

Ejecuta el siguiente comando en la raíz del proyecto para precargar la información:

```bash
# Ejecutar el script de precarga de datos (Seed)
python -m app.db.seed
```

Una vez ejecutado, tendrás los siguientes usuarios disponibles para probar el sistema de login:

| Username | Password | Rol | Nivel de Acceso |
|----------|----------|-----|-----------------|
| admin | Admin1234! | admin | Acceso total (ej. crear/borrar usuarios) |
| juan | Juan1234! | user | Acceso básico y rutas protegidas normales |

## Ejecución

```bash
uvicorn app.main:app --reload
```

API disponible en: `http://localhost:8000`

Documentación automática:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`



## Estructura del proyecto

```
seguridad_jwt_pg/
├── app/
│   ├── main.py              # Entry point FastAPI
│   ├── core/
│   │   ├── config.py        # Settings (pydantic-settings)
│   │   ├── database.py      # Engine PostgreSQL
│   │   ├── security.py      # JWT + bcrypt (hash/verify)
│   │   ├── deps.py          # Dependencias auth (OAuth2, require_role)
│   │   ├── uow.py           # Unit of Work
│   │   └── base_repository.py
│   ├── modules/
│   │   ├── usuarios/        # Auth, registro, RBAC
│   │   └── categorias/      # CRUD categorías
│   └── db/
│       └── seed.py          # Datos iniciales
├── seguridad_jwt.http       # REST Client (VS Code)
├── categorias_crud.http     # REST Client (VS Code)
├── requirements.txt
└── .env.example
```

## Quick start

### 1. Registrar un usuario

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"pepito","full_name":"Pepito Pérez","email":"pepito@example.com","password":"Password123!"}'
```

### 2. Obtener token JWT

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -d "username=pepito&password=Password123!"
```