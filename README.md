# 📚 API REST Biblioteca Central UNCP

## Integrantes

- INGRID ANDRADE EGOAVIL
- YARANGA RUIZ JOSUE

## Descripción

API RESTful desarrollada con Django REST Framework para la gestión de la Biblioteca Central de la UNCP. Permite la integración con el campus virtual, consulta de catálogo y gestión de préstamos.

## 🚀 Instalación y Ejecución

1. Clonar el repositorio: `git clone [URL_DE_TU_REPO]`
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Aplicar migraciones: `python manage.py migrate`
6. Poblar datos de prueba: `python populate_data.py`
7. Ejecutar servidor: `python manage.py runserver`

## 📖 Endpoints Principales

- `GET /api/libros/` - Listar libros (Público)
- `GET /api/libros/{id}/` - Detalle de libro
- `POST /api/prestamos/` - Registrar préstamo (Auth)
- `POST /api/prestamos/{id}/devolver/` - Marcar devolución
- `GET /api/usuarios/perfil/` - Perfil de usuario (Auth)

## 📚 Documentación

- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 🛠️ Decisiones de Diseño

- Se utilizó `AbstractUser` para personalizar el modelo de usuario según los roles de la UNCP.
- Se implementó `drf-spectacular` para la generación automática de OpenAPI 3.0.
- Los campos calculados como `disponible` y `multa` se manejan como `@property` en los modelos y `SerializerMethodField` o `ReadOnlyField` en los serializadores.
