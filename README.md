# Nacho Pizza Club - Sistema de Gestión Fullstack 

Este proyecto es una aplicación web completa desarrollada para el **Primer Parcial** de prog4 de la Tecnicatura Universitaria en Programación. Se trata de un sistema de gestión de catálogo para una pizzería, permitiendo administrar Categorías, Productos e Ingredientes con relaciones complejas.

##  Presentación en Video
> [!IMPORTANT]  
> **Link al Video (YouTube):** https://youtu.be/w6wwHA9IqMI  
> *Duración: < 15 minutos.*

##  Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework principal para la API.
- **SQLModel**: ORM para modelado y relaciones (1:N y N:N).
- **PostgreSQL**: Base de datos relacional.
- **Unit of Work & Repository Pattern**: Arquitectura limpia y modular.

### Frontend
- **React + TypeScript**: Biblioteca de UI y tipado estricto.
- **Vite**: Herramienta de construcción rápida.
- **TanStack Query (React Query)**: Gestión del estado del servidor y caché.
- **Tailwind CSS 4**: Diseño premium, responsive y minimalista.

##  Estructura del Repositorio
- `/Backend`: Código fuente de la API, modelos de datos y migraciones.
- `/Frontend`: Aplicación Single Page Application (SPA).
- `CHECKLIST.md`: Seguimiento de requisitos académicos.
- `uml del parcial.jpeg`: Diagrama de clases y relaciones.

##  Instalación y Uso

### Backend
1. Navegar a `/Backend`.
2. Crear entorno virtual: `python -m venv .venv`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Configurar `.env` con las credenciales de PostgreSQL.
5. Ejecutar: `fastapi dev app/main.py`.

### Frontend
1. Navegar a `/Frontend`.
2. Instalar dependencias: `npm install`.
3. Ejecutar: `npm run dev`.

---
