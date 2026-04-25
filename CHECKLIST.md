# Lista de Verificación del Proyecto Integrador - Nacho Pizza Club 🍕

## Backend (FastAPI + SQLModel)

- [x] Entorno: Uso de .venv, requirements.txt y FastAPI funcionando en modo dev.
- [x] Modelado: Tablas creadas con SQLModel incluyendo relaciones Relationship (1:N y N:N). (Implementado N:N para Categorías e Ingredientes).
- [x] Validación: Uso de Annotated, Query y Path para reglas de negocio (ej. gt=0, max_length).
- [x] CRUD Persistente: Endpoints funcionales para Crear, Leer, Actualizar y Borrar en PostgreSQL.
- [x] Seguridad de Datos: Implementación de response_model (Schemas) para segregación de datos.
- [x] Estructura: Código organizado por módulos (routers, schemas, services, models, unit_of_work).

---

## Frontend (React + TypeScript + Tailwind)

- [x] Setup: Proyecto creado con Vite + TS y estructura de carpetas modular.
- [x] Componentes: Uso de componentes funcionales y Props debidamente tipadas con interfaces.
- [x] Estilos: Interfaz construida íntegramente con clases de utilidad de Tailwind CSS 4 con diseño premium.
- [x] Navegación: Configuración de react-router-dom con rutas dinámicas (/products/:id).
- [x] Estado Local: Uso de useState para el manejo de formularios y estados de UI.

---

## Integración y Server State

- [x] Lectura (useQuery): Listados y detalles consumiendo datos reales de la API.
- [x] Escritura (useMutation): Formularios que envían datos al backend con éxito.
- [x] Sincronización: Uso de invalidateQueries para refrescar la UI automáticamente tras un cambio.
- [x] Feedback: Gestión visual de estados de "Cargando..." y "Error" en las peticiones.

---

## Video de Presentación

- [x] Duración: El video dura 15 minutos o menos.
- [x] Audio/Video: La voz es clara y la resolución de pantalla permite leer el código.
- [x] Demo: Se muestra el flujo completo desde la creación hasta la persistencia en la DB.

---

## Desafío Técnico Resuelto 💡
Implementé un sistema de **Borrado en Cascada Jerárquico** en el Backend. Al eliminar una categoría, el sistema busca recursivamente todos sus descendientes y los productos asociados para realizar un "soft-delete" consistente, asegurando que no queden datos huérfanos en la base de datos sin necesidad de configurar cascadas complejas a nivel de motor de DB.
