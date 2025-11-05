# 🚀 Microservices Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)

Laboratorio de arquitectura de microservicios con Django REST Framework, PostgreSQL y Redis. Proyecto educativo para aprender patrones de diseño, comunicación entre servicios y despliegue con Docker.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Servicios](#-servicios)
- [Tecnologías](#️-tecnologías)
- [Instalación Rápida](#-instalación-rápida)
- [Documentación](#-documentación)
- [Desarrollo](#-desarrollo)
- [Testing](#-testing)
- [Contribuir](#-contribuir)
- [Roadmap](#-roadmap)
- [Licencia](#-licencia)

## ✨ Características

- ✅ **Arquitectura de Microservicios**: Servicios independientes y desacoplados
- ✅ **Autenticación JWT**: Sistema seguro con access y refresh tokens
- ✅ **API RESTful**: Siguiendo mejores prácticas de diseño
- ✅ **Cache Redis**: Optimización de rendimiento
- ✅ **Procesamiento Asíncrono**: Celery para tareas en background
- ✅ **Containerización**: Todo en Docker para fácil deployment
- ✅ **Documentación OpenAPI**: Contratos de API versionados
- ✅ **Logging Estructurado**: JSON logs para monitoreo
- ✅ **Health Checks**: Endpoints de salud en cada servicio

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│                   Port: 3000 (futuro)                    │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│              Reverse Proxy (Nginx)                       │
│                   Port: 80 (futuro)                      │
└────┬──────────────┬────────────────┬────────────────────┘
     │              │                │
┌────▼────┐   ┌────▼────┐      ┌───▼──────┐
│  Auth   │   │  Blog   │      │  Email   │
│ Service │   │ Service │      │ Service  │
│  :8000  │   │  :8001  │      │  :8002   │
└────┬────┘   └────┬────┘      └────┬─────┘
     │             │                 │
┌────▼─────────────▼────┐      ┌────▼─────┐
│   PostgreSQL (DB)      │      │  Redis   │
│      Port: 5432        │      │  :6379   │
└────────────────────────┘      └──────────┘
                                      │
                                ┌─────▼─────┐
                                │  Celery   │
                                │  Worker   │
                                └───────────┘
```

**📖 [Ver documentación detallada de arquitectura](docs/ARCHITECTURE.md)**

### Descripción de Servicios

| Servicio | Puerto | Estado | Descripción |
|----------|--------|--------|-------------|
| **Auth Service** | 8000 | ✅ Completado | Autenticación JWT, gestión de usuarios |
| **Blog Service** | 8001 | ✅ Completado | CRUD de posts, categorías, búsqueda, cache |
| **Email Service** | 8002 | ✅ Completado | Notificaciones asíncronas con Celery |
| **PostgreSQL** | 5432 | ✅ Operativo | Base de datos relacional compartida |
| **Redis** | 6379 | ✅ Operativo | Cache + Message broker para Celery |
| **Frontend** | 3000 | 📋 Pendiente | Interfaz de usuario React |
| **Nginx** | 80 | 📋 Pendiente | Reverse proxy y load balancer |

## 🛠️ Tecnologías

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Backend | Django + DRF | 5.0 |
| Autenticación | JWT (SimpleJWT) | 5.3 |
| Base de datos | PostgreSQL | 15 |
| Caché | Redis | 7 |
| Frontend | React | 18.x |
| Proxy | Nginx | latest |
| Contenedores | Docker | latest |

## � Instalación Rápida

### Prerrequisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/) v3.9+
- [Git](https://git-scm.com/)
- 4GB RAM mínimo para los contenedores

### Configuración Inicial

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hernandz09/microservices-lab.git
cd microservices-lab

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env si necesitas cambiar configuraciones (opcional)

# 3. Levantar todos los servicios
docker compose up -d

# 4. Verificar que los contenedores estén corriendo
docker ps

# 5. Verificar salud de los servicios
curl http://localhost:8000/health  # Auth Service
curl http://localhost:8001/healthz  # Blog Service
curl http://localhost:8002/healthz  # Email Service
```

¡Listo! Los servicios estarán disponibles en:
- **Auth Service**: http://localhost:8000
- **Blog Service**: http://localhost:8001
- **Email Service**: http://localhost:8002

### Datos de Prueba

El Blog Service incluye datos de ejemplo (30 posts, 5 categorías, 3 autores) que se cargan automáticamente.

Para el Auth Service, puedes crear un usuario de prueba:

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## 🚀 Uso

### Comandos Útiles

```bash
# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Detener servicios
docker compose down

# Ver estado de contenedores
docker ps

# Reconstruir contenedores
docker compose up -d --build
```

### Acceso a los Servicios

- **PostgreSQL**: `localhost:5432`
  - Usuario: `devuser`
  - Contraseña: `devpass`
  - Base de datos: `main_db`

- **Redis**: `localhost:6379`

### Conexión a PostgreSQL

```bash
docker exec -it db_postgres psql -U devuser -d main_db
```

### Conexión a Redis

```bash
docker exec -it cache_redis redis-cli
```

## 📚 Documentación

- **[Arquitectura del Sistema](docs/ARCHITECTURE.md)** - Diagramas, patrones de diseño, flujos de datos
- **[Guía de Contribución](CONTRIBUTING.md)** - Cómo contribuir al proyecto
- **[Testing y Análisis](docs/testing/)** - Resultados de pruebas y análisis
- **[Screenshots](docs/screenshots/)** - Capturas de pantalla de funcionalidades

### Contratos de API (OpenAPI)

- [Auth Service](auth-service/README.md) - Endpoints de autenticación
- [Blog Service OpenAPI](blog-service/openapi.yaml) - Especificación completa
- [Email Service OpenAPI](email-service/openapi.yaml) - Especificación completa

### Colección de Postman

Importa `postman_collection.json` en Postman para probar todos los endpoints.

```bash
# O usa newman para tests automatizados
npm install -g newman
newman run postman_collection.json
```

## 💻 Desarrollo

### Estructura del Proyecto

```
microservices-lab/
├── auth-service/          # 🔐 Servicio de autenticación
├── blog-service/          # 📝 Servicio de blog
├── email-service/         # 📧 Servicio de notificaciones
├── frontend/              # ⚛️ Frontend React (futuro)
├── reverse-proxy/         # 🔀 Nginx proxy (futuro)
├── docs/                  # 📚 Documentación
│   ├── ARCHITECTURE.md
│   ├── screenshots/
│   └── testing/
├── docker-compose.yml     # 🐳 Orquestación
├── .env.example           # ⚙️ Variables de entorno
├── postman_collection.json # 🧪 Tests de API
├── CONTRIBUTING.md        # 🤝 Guía de contribución
├── LICENSE                # 📄 Licencia MIT
└── README.md
```

### Comandos de Desarrollo

```bash
# Reconstruir servicios después de cambios en código
docker compose up -d --build

# Ver logs de un servicio específico
docker compose logs -f auth
docker compose logs -f blog
docker compose logs -f email

# Acceder al shell de Django
docker compose exec auth python manage.py shell
docker compose exec blog python manage.py shell

# Ejecutar migraciones
docker compose exec auth python manage.py migrate
docker compose exec blog python manage.py migrate

# Crear superusuario (admin)
docker compose exec auth python manage.py createsuperuser
docker compose exec blog python manage.py createsuperuser

# Limpiar todo y empezar de cero
docker compose down -v  # Elimina volúmenes (⚠️ borra datos)
docker compose up -d --build
```

### Acceso al Admin de Django

- **Auth Service**: http://localhost:8000/admin/
- **Blog Service**: http://localhost:8001/admin/

## 🧪 Testing

### Tests Manuales con cURL

```bash
# Registro de usuario
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login (obtener tokens)
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'

# Listar posts
curl http://localhost:8001/api/posts/

# Buscar posts
curl "http://localhost:8001/api/posts/?search=microservices"

# Ver detalle de post
curl http://localhost:8001/api/posts/introduction-to-microservices-architecture/
```

### Tests Automatizados

```bash
# Tests unitarios de Django
docker compose exec auth python manage.py test
docker compose exec blog python manage.py test

# Coverage
docker compose exec auth coverage run --source='.' manage.py test
docker compose exec auth coverage report

# Tests con Postman/Newman
newman run postman_collection.json --environment env.json
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee la [Guía de Contribución](CONTRIBUTING.md) antes de enviar un PR.

### Proceso Rápido

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'feat: agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### Convención de Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(scope): add new feature
fix(scope): fix bug
docs: update documentation
test: add tests
refactor: refactor code
```

## ✅ Checklist Día 1

### Entregables

- [x] **Repo Git**: Subido a GitHub con estructura base y `.env.example`
- [x] **Docker Compose funcional**: Levanta PostgreSQL y Redis sin errores
- [x] **README documentado**: Incluye arquitectura y checklist
- [x] **Captura**: Mostrando los contenedores en ejecución (`docker ps`)

### Estructura Base Completada

```
microservices-lab/
├── .env.example          ✅ Configuración de ejemplo
├── .gitignore            ✅ Archivos ignorados
├── docker-compose.yml    ✅ Orquestación de contenedores
├── README.md             ✅ Documentación principal
├── postman_collection.json ✅ Colección de pruebas
├── docs/                 ✅ Documentación adicional
│   ├── screenshots/      ✅ Capturas de pantalla
│   └── testing/          ✅ Análisis y pruebas
├── auth-service/         ✅ Servicio de autenticación
├── blog-service/         ✅ Servicio de blog
├── email-service/        📋 Estructura base (pendiente)
├── frontend/             📋 Estructura base (pendiente)
└── reverse-proxy/        📋 Estructura base (pendiente)
```

### Verificación

Para verificar que todo funciona correctamente:

1. Los contenedores deben estar corriendo:
```bash
docker ps
```

2. PostgreSQL debe estar accesible:
```bash
docker exec -it db_postgres pg_isready
```

3. Redis debe estar accesible:
```bash
docker exec -it cache_redis redis-cli ping
```

---

## 🔐 Día 2: Auth Service

### Microservicio de Autenticación (Django + DRF + JWT)

El servicio de autenticación maneja usuarios, registro, login y tokens JWT de forma completamente independiente.

### 🏗️ Estructura del Servicio

```
auth-service/
├── auth_service/          # Proyecto Django principal
│   ├── settings.py       # Configuración (DB, Redis, JWT, CORS)
│   ├── urls.py           # Rutas principales
│   └── wsgi.py           # WSGI para Gunicorn
├── users/                # App de usuarios
│   ├── models.py         # Modelo User personalizado
│   ├── serializers.py    # Serializadores DRF
│   ├── views.py          # Vistas/Endpoints
│   ├── urls.py           # Rutas de la app
│   └── admin.py          # Configuración del admin
├── Dockerfile            # Imagen Docker
├── requirements.txt      # Dependencias Python
└── manage.py             # CLI de Django
```

### � Endpoints Implementados

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/register/` | Registro de nuevos usuarios | No |
| POST | `/api/token/` | Login - Obtener tokens JWT | No |
| POST | `/api/token/refresh/` | Refrescar access token | No |
| GET | `/api/me/` | Información del usuario autenticado | Sí (Bearer Token) |

### 📦 Dependencias Principales

```txt
django==5.0
djangorestframework==3.15
djangorestframework-simplejwt==5.3
psycopg2-binary
redis
django-cors-headers
gunicorn
```

### 🐳 Configuración Docker

El servicio corre en el puerto **8000** y se conecta a PostgreSQL y Redis.

```yaml
auth:
  build: ./auth-service
  container_name: auth_service
  ports:
    - "8000:8000"
  depends_on:
    - postgres
    - redis
```

### 🧪 Pruebas con Postman

#### 1. Registro de Usuario

![Registro de Usuario](docs/screenshots/day2-register.png)

**Request:**
```json
POST http://localhost:8000/api/register/

{
  "email": "Pedro@example.com",
  "password": "mipassword12345",
  "password2": "mipassword12345",
  "first_name": "Pedro",
  "last_name": "Hernandez"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 2,
    "email": "Pedro@example.com",
    "first_name": "Pedro",
    "last_name": "Hernandez",
    "date_joined": "2025-10-27T13:36:11.542814Z"
  },
  "message": "Usuario registrado exitosamente"
}
```

---

#### 2. Login - Obtener Tokens JWT

![Login con JWT](docs/screenshots/day2-login.png)

**Request:**
```json
POST http://localhost:8000/api/token/

{
  "email": "Pedro@example.com",
  "password": "mipassword12345"
}
```

**Response:** `200 OK`
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMDExNzQyMCwiaWF0IjoxNzMwMDMxMDIwLCJqdGkiOiI4ZTNiNWRiYjE3NDFlYjI4MDk2M2IyNmNkYWU3ZmI5ZCIsInVzZXJfaWQiOjJ9.DobfgnKyaDXBjYU8bPCUZfLu7QJgfJFIZT4T_sYyvIwQ",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMDM0NjIwLCJpYXQiOjE3MzAwMzEwMjAsImp0aSI6IjRlNjY0YmM5Yjc4MDljOGJiZmU3ZTE3OWE5YzRlYjNjIiwidXNlcl9pZCI6Mn0.FINjQyNwFNhMZNzZhNjM1MjU5M2NIIwIzYwZ1CIG1n0.DobfgnKyaDXBjYU8bPCUZfLu7QJgjFIZT4T_sYyLIwQ"
}
```

---

#### 3. Perfil del Usuario Autenticado

![Endpoint /api/me/](docs/screenshots/day2-me-endpoint.png)

**Request:**
```http
GET http://localhost:8000/api/me/
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 2,
  "email": "Pedro@example.com",
  "first_name": "Pedro",
  "last_name": "Hernandez",
  "date_joined": "2025-10-27T13:36:11.542814Z"
}
```

---

### 🐳 Contenedores en Ejecución

![Docker PS](docs/screenshots/day2-docker-ps.png)

```bash
CONTAINER ID   IMAGE                    COMMAND                  STATUS                   PORTS                    NAMES
699e146b52f0   microservices-lab-auth   "sh -c 'python manag…"   Up 12 minutes           0.0.0.0:8000->8000/tcp   auth_service
60946ff593b9   postgres:15              "docker-entrypoint.s…"   Up 13 minutes (healthy)  0.0.0.0:5432->5432/tcp   db_postgres
6250f2d1d03c   redis:7                  "docker-entrypoint.s…"   Up 13 minutes (healthy)  0.0.0.0:6379->6379/tcp   cache_redis
```

### ✅ Checklist Día 2

- [x] **Código funcional**: Microservicio auth-service con Django + JWT
- [x] **Modelo User personalizado**: Extiende AbstractBaseUser con email como USERNAME_FIELD
- [x] **Endpoints implementados**: register, token, token/refresh, me
- [x] **Docker funcionando**: Contenedor corriendo en puerto 8000
- [x] **Migraciones aplicadas**: Base de datos configurada correctamente
- [x] **Pruebas Postman**: Registro, login, autenticación y refresh validados
- [x] **Conexión PostgreSQL**: Configurada con variables de entorno
- [x] **Conexión Redis**: Cache configurado y funcional
- [x] **CORS habilitado**: Para comunicación con frontend
- [x] **Documentación**: README actualizado con endpoints y ejemplos

### 🔧 Comandos Útiles

```bash
# Reconstruir el servicio auth
docker compose build auth

# Levantar todos los servicios
docker compose up -d

# Ver logs del servicio auth
docker logs auth_service -f

# Ejecutar migraciones
docker exec -it auth_service python manage.py migrate

# Crear superusuario
docker exec -it auth_service python manage.py createsuperuser

# Acceder al shell de Django
docker exec -it auth_service python manage.py shell

# Acceder al admin de Django
# http://localhost:8000/admin/
```

### 📚 Recursos de Referencia

- Video guía: [Microservicios con Django REST Framework](https://www.youtube.com/watch?v=wj766sxHZrM) (26:13 - 2:54:00)
- Documentación: [Django REST Framework](https://www.django-rest-framework.org/)
- Documentación: [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

## �️ Roadmap

### ✅ Fase 1: Fundamentos (Completado)
- [x] Configuración de Docker Compose
- [x] PostgreSQL y Redis
- [x] Auth Service con JWT
- [x] Blog Service con cache
- [x] Email Service con Celery

### 🚧 Fase 2: Integración (En Progreso)
- [ ] Validación de JWT entre servicios
- [ ] Endpoints protegidos (POST/PUT/DELETE)
- [ ] Roles y permisos
- [ ] Tests end-to-end

### 📋 Fase 3: Frontend (Planeado)
- [ ] Frontend React + Vite
- [ ] Autenticación con JWT
- [ ] CRUD de posts
- [ ] Gestión de perfil

### 📋 Fase 4: Producción (Planeado)
- [ ] Reverse Proxy Nginx
- [ ] HTTPS/SSL
- [ ] CI/CD con GitHub Actions
- [ ] Monitoreo con Prometheus + Grafana
- [ ] Deploy en cloud (AWS/GCP)

**Ver roadmap completo**: [GitHub Projects](https://github.com/Hernandz09/microservices-lab/projects)

---

<details>
<summary><h2>📝 Día 3: Blog Service (Histórico)</h2></summary>

### Microservicio de Blog (Django + DRF + PostgreSQL + Redis)

Microservicio completo para gestión de posts, categorías y autores con búsqueda, paginación y caché.

### 🏗️ Estructura del Servicio

```
blog-service/
├── blog_service/          # Proyecto Django principal
│   ├── settings.py       # Configuración
│   └── urls.py           # Rutas principales
├── core/                 # Utilidades compartidas
│   ├── middleware.py     # Logging + Auth header capture
│   ├── logging.py        # JSON formatter
│   └── views.py          # Healthcheck
├── categories/           # App de categorías
│   ├── models.py         # Category model
│   ├── serializers.py
│   ├── views.py          # CategoryViewSet (cached)
│   └── urls.py
├── authors/             # App de autores
│   ├── models.py         # Author model
│   └── serializers.py
├── posts/               # App de posts
│   ├── models.py         # Post model
│   ├── serializers.py    # List & Detail serializers
│   ├── views.py          # PostViewSet con búsqueda
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_blog.py  # Comando de seeding
├── Dockerfile
├── requirements.txt
├── openapi.yaml         # Contrato API
└── README.md
```

### 🎯 Características Implementadas

- ✅ **Modelos**: Category, Author, Post con relaciones FK
- ✅ **Endpoints públicos**: GET para categorías y posts
- ✅ **Búsqueda**: Full-text en título y contenido de posts
- ✅ **Paginación**: 10 posts por página
- ✅ **Caché Redis**:
  - Categorías: 60 segundos TTL
  - Detalle de post: 120 segundos TTL
- ✅ **Contador de vistas**: Incremento automático al ver posts
- ✅ **Health Check**: Verifica DB y Redis
- ✅ **Logging estructurado**: JSON logs por request
- ✅ **Seed de datos**: 5 categorías, 3 autores, 30 posts
- ✅ **OpenAPI contract**: Documentación completa de la API
- ✅ **Preparado para JWT**: Middleware que captura Authorization header

### 🚀 Endpoints Disponibles

| Método | Endpoint | Descripción | Caché |
|--------|----------|-------------|-------|
| GET | `/healthz` | Health check (DB + Redis) | No |
| GET | `/api/categories` | Lista de categorías activas | 60s |
| GET | `/api/posts` | Lista de posts (paginado) | No |
| GET | `/api/posts?search=texto` | Búsqueda de posts | No |
| GET | `/api/posts/{slug}` | Detalle de post | 120s |

### 🐳 Configuración Docker

El servicio corre en el puerto **8001** y se conecta a PostgreSQL y Redis compartidos.

```yaml
blog:
  build: ./blog-service
  container_name: blog_service
  ports:
    - "8001:8001"
  depends_on:
    - postgres
    - redis
```

### 📊 Datos de Ejemplo (Seed)

El comando `seed_blog` se ejecuta automáticamente al iniciar y crea:

- **5 categorías**: Technology, Programming, DevOps, Cloud Computing, Security
- **3 autores**: John Developer, Jane Architect, Mike DevOps
- **30 posts**: 20 publicados y 10 borradores
  - Posts publicados con fechas variadas (últimos 60 días)
  - Contador de vistas aleatorio (50-5000)

### 🧪 Ejemplos de Uso

#### 1. Health Check

```bash
curl http://localhost:8001/healthz
```

**Respuesta:**
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

#### 2. Listar Categorías (Cacheado 60s)

```bash
curl http://localhost:8001/api/categories
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Technology",
    "slug": "technology"
  },
  {
    "id": 2,
    "name": "Programming",
    "slug": "programming"
  }
]
```

#### 3. Listar Posts con Paginación

```bash
curl http://localhost:8001/api/posts
```

**Respuesta:**
```json
{
  "count": 20,
  "next": "http://localhost:8001/api/posts?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Microservices Architecture",
      "slug": "introduction-to-microservices-architecture",
      "excerpt": "Microservices architecture is a design pattern...",
      "author": {
        "id": 1,
        "display_name": "John Developer",
        "email": "john.dev@example.com"
      },
      "category": {
        "id": 1,
        "name": "Technology",
        "slug": "technology"
      },
      "published_at": "2025-10-15T10:30:00Z",
      "views": 1250
    }
  ]
}
```

#### 4. Buscar Posts

```bash
curl "http://localhost:8001/api/posts?search=docker"
```

#### 5. Ver Detalle de Post (Cacheado 120s, incrementa views)

```bash
curl http://localhost:8001/api/posts/introduction-to-microservices-architecture
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Introduction to Microservices Architecture",
  "slug": "introduction-to-microservices-architecture",
  "body": "Full content of the post...",
  "excerpt": "Microservices architecture is a design pattern...",
  "author": {
    "id": 1,
    "display_name": "John Developer",
    "email": "john.dev@example.com"
  },
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology"
  },
  "status": "published",
  "published_at": "2025-10-15T10:30:00Z",
  "views": 1251,
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-10-15T10:00:00Z"
}
```

### 🗄️ Modelos de Base de Datos

**Category**
- `id`, `name` (único), `slug` (auto-generado), `is_active`
- `created_at`, `updated_at`

**Author**
- `id`, `display_name`, `email` (único), `bio`, `is_active`
- `created_at`, `updated_at`

**Post**
- `id`, `title`, `slug` (auto-generado), `body`, `excerpt` (auto-generado)
- `author` (FK), `category` (FK)
- `status` (draft/published), `views`, `published_at`
- `created_at`, `updated_at`

### ✅ Checklist Día 3

- [x] **Proyecto Django configurado**: Settings, apps, middleware
- [x] **Modelos implementados**: Category, Author, Post
- [x] **Serializers DRF**: List y Detail serializers
- [x] **ViewSets con features**:
  - [x] Paginación (10 items/página)
  - [x] Búsqueda full-text
  - [x] Filtros por status
- [x] **Caché Redis**:
  - [x] Categorías (60s TTL)
  - [x] Detalle de posts (120s TTL)
- [x] **Comando seed_blog**: 30 posts de ejemplo
- [x] **Health check**: Endpoint `/healthz`
- [x] **Logging estructurado**: Formato JSON
- [x] **Middlewares**:
  - [x] Request logging
  - [x] Auth header logging (prep. Día 4)
- [x] **Docker**:
  - [x] Dockerfile optimizado
  - [x] docker-compose.yml actualizado
  - [x] Servicio en puerto 8001
- [x] **Documentación**:
  - [x] openapi.yaml con contrato completo
  - [x] README detallado con ejemplos
  - [x] Ejemplos de cURL

### 🔧 Comandos Útiles

```bash
# Levantar el servicio blog
docker-compose up -d blog

# Ver logs en tiempo real
docker-compose logs -f blog

# Ejecutar seed de datos
docker-compose exec blog python manage.py seed_blog

# Shell de Django
docker-compose exec blog python manage.py shell

# Crear superusuario
docker-compose exec blog python manage.py createsuperuser

# Acceder al admin: http://localhost:8001/admin/

# Verificar caché Redis
docker-compose exec redis redis-cli
> KEYS *
> TTL "clave_aqui"

# Limpiar caché
docker-compose exec redis redis-cli FLUSHALL

# Reiniciar servicio
docker-compose restart blog
```

### 🔐 Preparación para Día 4

El servicio ya está preparado para integración JWT:

1. ✅ **Middleware `AuthTokenLoggingMiddleware`**: Captura y loguea headers `Authorization`
2. ✅ **Esqueleto en OpenAPI**: Definición de `BearerAuth`
3. ✅ **ViewSets públicos**: Listos para agregar permisos DRF

**Próximos pasos (Día 4)**:
- Validar JWT desde Auth Service
- Proteger endpoints POST/PUT/DELETE
- Enlazar autores con usuarios de Auth Service
- Implementar permisos basados en roles

### 📄 Contrato API

El contrato completo está en `blog-service/openapi.yaml`.

Puedes visualizarlo en [Swagger Editor](https://editor.swagger.io/) copiando el contenido del archivo.

---

</details>

## � Estadísticas del Proyecto

- **Servicios**: 3 microservicios + 2 bases de datos
- **Endpoints**: 15+ endpoints REST
- **Líneas de código**: ~3,000+ (Python)
- **Tests**: Coverage > 80% (objetivo)
- **Tiempo de setup**: < 5 minutos

## 🎓 Aprendizajes

Este proyecto cubre:

- ✅ Arquitectura de microservicios
- ✅ API REST con Django REST Framework
- ✅ Autenticación JWT
- ✅ Caché con Redis
- ✅ Procesamiento asíncrono con Celery
- ✅ Containerización con Docker
- ✅ Orquestación con Docker Compose
- ✅ Logging estructurado
- ✅ Health checks
- ✅ OpenAPI/Swagger documentation

## 🐛 Problemas Conocidos

Ver [Issues](https://github.com/Hernandz09/microservices-lab/issues) para reportar bugs o solicitar features.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Ignacio Hernandez**
- GitHub: [@Hernandz09](https://github.com/Hernandz09)
- LinkedIn: [Tu perfil](https://linkedin.com)

## 🙏 Agradecimientos

- [Django REST Framework](https://www.django-rest-framework.org/) por el excelente framework
- [Docker](https://www.docker.com/) por simplificar el deployment
- Comunidad de Python y Django por los recursos educativos

## ⭐ Star History

Si este proyecto te ha sido útil, ¡considera darle una estrella! ⭐

---

<div align="center">

🎓 **Microservices Lab** - Proyecto educativo de arquitectura de microservicios

Hecho con ❤️ y ☕ por [Ignacio Hernandez](https://github.com/Hernandz09)

</div>
