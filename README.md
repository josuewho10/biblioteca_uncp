# 📚 API REST – Biblioteca Central UNCP

API RESTful desarrollada con **Django REST Framework** para la gestión de los servicios de la Biblioteca Central de la Universidad Nacional del Centro del Perú (UNCP).

## 👥 Integrantes

- **ANDRADE EGOAVIL, INGRID**
- **YARANGA RUIZ, JOSUE**

## 📌 Descripción del proyecto

El proyecto consiste en el desarrollo de una API RESTful que permite gestionar y consultar los recursos y servicios de la Biblioteca Central de la UNCP.

La API proporciona funcionalidades para la consulta del catálogo bibliográfico, administración de usuarios y gestión de préstamos y devoluciones. Asimismo, contempla la integración con el campus virtual mediante servicios web.

### Funcionalidades principales

- Consulta del catálogo de libros.
- Visualización de información detallada de cada libro.
- Registro y gestión de préstamos.
- Procesamiento de devoluciones.
- Consulta del perfil de usuario.
- Control de acceso mediante autenticación.

## 🛠️ Tecnologías utilizadas

| Tecnología                         | Descripción                             |
| ---------------------------------- | --------------------------------------- |
| Python                             | Lenguaje de programación                |
| Django                             | Framework de desarrollo web             |
| Django REST Framework              | Construcción de API REST                |
| drf-spectacular                    | Generación de documentación OpenAPI 3.0 |
| SQLite / Base de datos configurada | Persistencia de información             |

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone [URL_DE_TU_REPOSITORIO]
cd [NOMBRE_DEL_PROYECTO]
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Cargar datos de prueba

```bash
python populate_data.py
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Una vez iniciado, el servidor estará disponible en:

```text
http://127.0.0.1:8000/
```

## 📖 Endpoints principales

Los siguientes endpoints representan las operaciones principales disponibles en la API.

| Método | Endpoint                        | Descripción                   | Acceso      |
| ------ | ------------------------------- | ----------------------------- | ----------- |
| GET    | `/api/libros/`                  | Listar libros                 | Público     |
| GET    | `/api/libros/{id}/`             | Consultar detalle de un libro | Público     |
| POST   | `/api/prestamos/`               | Registrar un préstamo         | Autenticado |
| POST   | `/api/prestamos/{id}/devolver/` | Registrar devolución          | Autenticado |
| GET    | `/api/usuarios/perfil/`         | Consultar perfil del usuario  | Autenticado |

> **Nota:** Los endpoints protegidos requieren las credenciales o el mecanismo de autenticación configurado en el proyecto.

## 📑 Documentación de la API

El proyecto incorpora documentación interactiva para facilitar la exploración y prueba de los servicios REST.

- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`

Para acceder desde el navegador:

```text
http://127.0.0.1:8000/api/docs/
http://127.0.0.1:8000/api/redoc/
```

## 🏗️ Decisiones de diseño e implementación

Durante el desarrollo se consideraron las siguientes decisiones técnicas:

### 1. Personalización del modelo de usuario

Se utilizó `AbstractUser` de Django para extender el modelo de usuario predeterminado y adaptarlo a las necesidades del sistema, permitiendo incorporar información y roles específicos.

### 2. Documentación mediante OpenAPI

Se implementó `drf-spectacular` para generar automáticamente la documentación de la API bajo el estándar OpenAPI 3.0, facilitando la comprensión y el consumo de los endpoints.

### 3. Uso de propiedades calculadas

Los atributos derivados, como `disponible` y `multa`, se gestionan mediante propiedades (`@property`) en los modelos. Posteriormente, se exponen en los serializadores utilizando `ReadOnlyField` o `SerializerMethodField`, según corresponda.

### 4. Separación de responsabilidades

Se aprovecha la arquitectura de Django REST Framework para separar la lógica de los modelos, serializadores y vistas, favoreciendo la organización y el mantenimiento del código.

---

## 🎓 Contexto académico

**Universidad:** Universidad Nacional del Centro del Perú (UNCP)  
**Proyecto:** API REST – Biblioteca Central UNCP  
**Desarrollo:** Trabajo colaborativo
