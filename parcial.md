# TECNICATURA UNIVERSITARIA  
# EN PROGRAMACIÓN  

---

## Primer Parcial  

**Objetivo:** Demostrar el funcionamiento de una aplicación Fullstack (FastAPI + React)  
que integre persistencia de datos, relaciones complejas, gestión de estado de servidor  
y navegación.  

---

## Requerimientos del Video  

- Duración máxima: 15 minutos.  
- Formato: Grabación de pantalla con voz en off (pueden usar herramientas como Loom, OBS o Clipchamp).  
- Contenido: El video debe dividirse en tres secciones: Arquitectura Backend, Interfaz Frontend y Demo de Flujo Completo.  

---

## Estructura de la Presentación  

### 1. Backend: El Corazón de la API (4-5 minutos)  

- Módulos a realizar: Categoría, ProductoCategoria, Producto, Ingrediente, ProductoIngrediente  

- Modelado de Datos: Muestra tus clases de SQLModel. Explica cómo implementaste la relación 1:N (ej. Categoría ↔ Producto) y la N:N (ej. Producto ↔ Etiqueta), mencionando el uso de Relationship y back_populates.  

- Endpoints y Lógica: Muestra un endpoint que utilice Annotated y Query para filtros o paginación. Explica brevemente cómo manejas las excepciones (HTTPException) y los códigos de estado.  

- Persistencia: Breve vistazo a la conexión con PostgreSQL y cómo se ven las tablas reflejadas (puedes mostrar pgAdmin o DBeaver).  

---

### Frontend: Experiencia de Usuario y Estado (4-5 minutos)  

- Módulos a realizar: Categorias, Ingredientes y productos, cada módulo debe tener su respectiva página, con su tabla sus botones de acciones y su respectivo modal con el formulario de alta y edición.  

- Estructura y Tipado: Muestra un componente clave y su respectiva interfaz en TypeScript para las Props.  

- Server State (TanStack Query): Explica una implementación de useQuery para el listado y una useMutation para el alta o edición. Muestra dónde haces la invalidación de la caché (invalidateQueries).  

- Navegación: Muestra la configuración de react-router-dom y cómo pasas parámetros dinámicos a través de la URL (ej. el ID para ver el detalle).  

---

### Demo en Vivo: El Flujo Integrador (5 minutos)  

- CRUD Completo: Crea un nuevo registro, edítalo y elimínalo mientras muestras la consola del navegador o la terminal del backend para validar las peticiones.  

- Validaciones: Intenta cargar datos inválidos para demostrar que las validaciones de Pydantic y los mensajes de error en el Frontend funcionan correctamente.  

- Relaciones en la UI: Muestra cómo se visualizan los datos relacionados (ej. "Este producto pertenece a la categoría X y tiene las etiquetas A y B").  

---

## Criterios de Evaluación  

1. Claridad Técnica: Uso correcto de la terminología vista en clase.  
2. Integración: El frontend debe consumir datos reales del backend (no mock data).  
3. Diseño: Aplicación coherente de Tailwind CSS para una interfaz limpia y responsive.  
4. Resolución de Problemas: Explicación de algún desafío técnico que encontraron y cómo lo resolvieron.  

---

## Entrega  

- Link: Subir el video a YouTube (como oculto/unlisted) o Drive (con permisos de lectura).  
- Código: Adjuntar link al repositorio de GitHub/GitLab con el README.md configurado y el archivo requirements.txt incluido.  

---

# Guía para el archivo CHECKLIST.md  

Copia el siguiente contenido en un archivo llamado CHECKLIST.md en la raíz de tu repositorio. Marca con una [x] los puntos que hayas completado y asegúrate de que todos funcionen antes de grabar tu video.  

---

## Lista de Verificación del Proyecto Integrador  

### Backend (FastAPI + SQLModel)  

- [ ] Entorno: Uso de .venv, requirements.txt y FastAPI funcionando en modo dev.  
- [ ] Modelado: Tablas creadas con SQLModel incluyendo relaciones Relationship (1:N y N:N).  
- [ ] Validación: Uso de Annotated, Query y Path para reglas de negocio (ej. longitudes, rangos).  
- [ ] CRUD Persistente: Endpoints funcionales para Crear, Leer, Actualizar y Borrar en PostgreSQL.  
- [ ] Seguridad de Datos: Implementación de response_model para no filtrar datos sensibles o innecesarios.  
- [ ] Estructura: Código organizado por módulos (routers, schemas, services, models, uow).  

---

### Frontend (React + TypeScript + Tailwind)  

- [ ] Setup: Proyecto creado con Vite + TS y estructura de carpetas limpia.  
- [ ] Componentes: Uso de componentes funcionales y Props debidamente tipadas con interfaces.  
- [ ] Estilos: Interfaz construida íntegramente con clases de utilidad de Tailwind CSS 4.  
- [ ] Navegación: Configuración de react-router-dom con al menos una ruta dinámica (ej. /detalle/:id).  
- [ ] Estado Local: Uso de useState para el manejo de formularios o UI interactiva.  

---

### Integración y Server State  

- [ ] Lectura (useQuery): Listados y detalles consumiendo datos reales de la API.  
- [ ] Escritura (useMutation): Formularios que envían datos al backend con éxito.  
- [ ] Sincronización: Uso de invalidateQueries para refrescar la UI automáticamente tras un cambio.  
- [ ] Feedback: Gestión visual de estados de "Cargando..." y "Error" en las peticiones.  

---

### Video de Presentación  

- [ ] Duración: El video dura 15 minutos o menos.  
- [ ] Audio/Video: La voz es clara y la resolución de pantalla permite leer el código.  
- [ ] Demo: Se muestra el flujo completo desde la creación hasta la persistencia en la DB.  

---

## Tips para los alumnos:  

- No mientas en el checklist: Si un punto no funciona, es mejor dejarlo vacío y explicar en el video qué intentaste hacer. La honestidad técnica se valora.  
- Orden del video: Sigue el mismo orden de este checklist para que tu presentación sea lógica y fácil de seguir para el evaluador.  

---

# Rúbrica de Calificación  

| Criterio | Logrado (1.5 - 2.0 pts) | En Proceso (0.5 - 1.4 pts) | No Logrado (0 - 0.4 pts) |
|--------|-------------------------|---------------------------|--------------------------|
| Arquitectura Backend (FastAPI & SQLModel) | Define modelos con SQLModel, usa Relationship (1:N y N:N) correctamente y aplica validaciones con Annotated/Query. | Los modelos son planos o las relaciones no están bien vinculadas en la lógica de la API. | No usa SQLModel, no hay relaciones o la API no funciona según lo solicitado. |
| Persistencia y CRUD (PostgreSQL) | CRUD completo y funcional contra la DB. Maneja correctamente los response_model y códigos de estado (201, 204, 404). | El CRUD funciona parcialmente o no se segregan correctamente los modelos de entrada/salida. | Solo tiene un CRUD en memoria o la conexión a la base de datos falla. |
| Frontend y Estado (React & TanStack) | Implementa useQuery y useMutation con invalidación de caché. Tipado de props y estados con TypeScript sin errores. | Usa fetch manual en lugar de TanStack Query o el tipado es inconsistente (abuso de any). | No hay integración con la API o el estado no se actualiza tras las mutaciones. |
| Navegación y UI (Router & Tailwind) | Estructura SPA funcional con rutas dinámicas (useParams). Diseño limpio y responsive con Tailwind CSS 4. | La navegación es errática o el diseño con Tailwind es pobre y carece de estructura (cards, formularios). | No usa React Router o el diseño no aplica clases de utilidad de Tailwind. |
| Calidad de Presentación (Video) | Explicación técnica fluida, demuestra el flujo completo y justifica decisiones de código en el tiempo estipulado. | El video es confuso, excede los 15 min o solo muestra la UI sin explicar el código fuente. | No entrega video o el contenido no coincide con el código entregado. |

---

# Guía de Puntuación Final  

- 9 - 10 (Excelente): Cumple con todos los criterios. El código es profesional, está modularizado (folders por módulos) y la demo es impecable.  
- 7 - 8 (Muy Bueno): La aplicación es funcional y cumple los requisitos técnicos, aunque puede tener detalles menores en el estilo o alguna validación faltante.  
- 4 - 6 (Aprobado): Cumple con la funcionalidad básica del CRUD y la persistencia, pero falla en la complejidad de las relaciones o en el manejo avanzado de TanStack Query.  
- 1 - 3 (Insuficiente): El proyecto no integra las dos partes (Back/Front) o tiene errores críticos de ejecución.  

---

## Entrega  

Debe entregar el link al repositorio en el campus, este repositorio el readme debe tener la descripción del proyecto y el link al video  