# Blog Service 📝

Microservicio de blog construido con Django REST Framework, PostgreSQL y Redis.

## 🎯 Características

- **Gestión de Posts**: CRUD de posts con estados (draft/published)
- **Categorías**: Organización de posts por categorías
- **Autores**: Sistema de autores (local por ahora, integración con Auth Service en Día 4)
- **Búsqueda**: Búsqueda full-text en títulos y contenido
- **Paginación**: 10 posts por página
- **Caché Redis**: Categorías (60s) y detalle de posts (120s)
- **Contador de vistas**: Incremento automático al ver posts
- **Health Check**: Monitoreo de DB y Redis
- **Logging estructurado**: Logs en formato JSON

## 🏗️ Stack Tecnológico

- **Framework**: Django 5.0 + Django REST Framework 3.15
- **Base de datos**: PostgreSQL 15
- **Caché**: Redis 7
- **Servidor**: Gunicorn
- **Containerización**: Docker

## 📦 Estructura del Proyecto

```
blog-service/
├── blog_service/          # Proyecto Django principal
│   ├── settings.py        # Configuración
│   ├── urls.py           # Rutas principales
│   ├── wsgi.py
│   └── asgi.py
├── core/                  # Utilidades compartidas
│   ├── middleware.py     # Request logging + Auth header logging
│   ├── logging.py        # JSON formatter
│   └── views.py          # Healthcheck
├── categories/            # App de categorías
│   ├── models.py         # Category model
│   ├── serializers.py
│   ├── views.py          # CategoryViewSet (cached)
│   └── urls.py
├── authors/              # App de autores
│   ├── models.py         # Author model
│   └── serializers.py
├── posts/                # App de posts
│   ├── models.py         # Post model
│   ├── serializers.py    # List & Detail serializers
│   ├── views.py          # PostViewSet con búsqueda
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_blog.py  # Comando de seeding
├── Dockerfile
├── requirements.txt
├── openapi.yaml          # Contrato API
└── README.md
```

## 🚀 Instalación y Ejecución

### Prerequisitos

- Docker y Docker Compose
- Variables de entorno configuradas en `.env`

### Quick Start

#### 1. Levantar el servicio con Docker Compose

Desde el directorio raíz del proyecto:

```bash
docker-compose up -d blog
```

Esto levantará automáticamente:
- PostgreSQL
- Redis
- Blog Service (con migraciones y seed automático)

El servicio estará disponible en: **http://localhost:8001**

#### 2. Verificar que el servicio está funcionando

```bash
# Health check
curl http://localhost:8001/healthz

# Debería retornar:
# {
#   "status": "healthy",
#   "checks": {
#     "database": "ok",
#     "redis": "ok"
#   }
# }
```

#### 3. Verificar contenedores corriendo

```bash
# Ver los contenedores corriendo
docker ps

# Deberías ver:
# - db_postgres (healthy)
# - cache_redis (healthy)
# - blog_service (running)
```

#### 4. El seed se ejecuta automáticamente

El comando `seed_blog` se ejecuta automáticamente al iniciar el contenedor.

Para ejecutarlo manualmente:

```bash
docker-compose exec blog python manage.py seed_blog
```

#### 5. Pruebas básicas

```bash
# Listar categorías
curl http://localhost:8001/api/categories

# Listar posts
curl http://localhost:8001/api/posts

# Buscar posts sobre "docker"
curl "http://localhost:8001/api/posts?search=docker"

# Ver detalle de un post
curl http://localhost:8001/api/posts/introduction-to-microservices-architecture
```

## 📊 Datos de Seed

El comando `seed_blog` crea:

- **5 categorías**: Technology, Programming, DevOps, Cloud Computing, Security
- **3 autores**: John Developer, Jane Architect, Mike DevOps
- **30 posts**: 20 publicados y 10 borradores
  - Posts publicados tienen fechas variadas (últimos 60 días)
  - Contador de vistas aleatorio (50-5000)

## 🔌 API Endpoints

### Health Check

```bash
GET /healthz
```

**Respuesta**:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

### Categorías

```bash
# Listar categorías (cached 60s)
GET /api/categories
```

**Respuesta**:
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

### Posts

```bash
# Listar posts (paginado, 10 por página)
GET /api/posts

# Buscar posts
GET /api/posts?search=microservices

# Paginar
GET /api/posts?page=2

# Combinar búsqueda y paginación
GET /api/posts?search=docker&page=1
```

**Respuesta**:
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

```bash
# Detalle de post (cached 120s, incrementa views)
GET /api/posts/{slug}
```

**Respuesta**:
```json
{
  "id": 1,
  "title": "Introduction to Microservices Architecture",
  "slug": "introduction-to-microservices-architecture",
  "body": "Full post content here...",
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

## 🧪 Ejemplos de cURL

### Listar todas las categorías

```bash
curl -X GET http://localhost:8001/api/categories
```

### Listar posts (primera página)

```bash
curl -X GET http://localhost:8001/api/posts
```

### Buscar posts sobre "Docker"

```bash
curl -X GET "http://localhost:8001/api/posts?search=docker"
```

### Obtener segunda página de posts

```bash
curl -X GET "http://localhost:8001/api/posts?page=2"
```

### Ver detalle de un post

```bash
curl -X GET http://localhost:8001/api/posts/introduction-to-microservices-architecture
```

### Health check

```bash
curl -X GET http://localhost:8001/healthz
```

### Con Authorization header (preparación para Día 4)

```bash
curl -X GET http://localhost:8001/api/posts \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

> **Nota**: Por ahora el header solo se loguea, no se valida. La integración con Auth Service se hará en el Día 4.

## 🔍 Caché Redis

### Endpoints cacheados:

1. **GET /api/categories** - TTL: 60 segundos
2. **GET /api/posts/{slug}** - TTL: 120 segundos

### Verificar caché manualmente:

```bash
# Conectarse a Redis
docker-compose exec redis redis-cli

# Ver todas las claves
KEYS *

# Ver TTL de una clave
TTL "clave_aqui"

# Limpiar toda la caché
FLUSHALL
```

## 📝 Logging

El servicio emite logs estructurados en JSON:

```json
{
  "timestamp": "2025-10-28T12:00:00.000000",
  "level": "INFO",
  "logger": "django.request",
  "message": "{\"method\": \"GET\", \"path\": \"/api/posts\", \"status_code\": 200, \"duration_ms\": 45.23}"
}
```

Ver logs en tiempo real:

```bash
docker-compose logs -f blog
```

## 🛠️ Comandos Útiles

```bash
# Ver logs
docker-compose logs -f blog

# Ejecutar migraciones
docker-compose exec blog python manage.py migrate

# Re-ejecutar seed
docker-compose exec blog python manage.py seed_blog

# Shell de Django
docker-compose exec blog python manage.py shell

# Crear superusuario para Django Admin
docker-compose exec blog python manage.py createsuperuser

# Acceder al admin en: http://localhost:8001/admin/

# Entrar al contenedor
docker-compose exec blog bash

# Reiniciar el servicio
docker-compose restart blog

# Reconstruir el contenedor
docker-compose up -d --build blog
```

## 🗄️ Modelos de Base de Datos

### Category
- `id`: AutoField
- `name`: CharField (único)
- `slug`: SlugField (único, auto-generado)
- `is_active`: BooleanField
- `created_at`, `updated_at`: DateTimeField

### Author
- `id`: AutoField
- `display_name`: CharField
- `email`: EmailField (único)
- `bio`: TextField
- `is_active`: BooleanField
- `created_at`, `updated_at`: DateTimeField

### Post
- `id`: AutoField
- `title`: CharField
- `slug`: SlugField (único, auto-generado)
- `body`: TextField
- `excerpt`: TextField (auto-generado desde body)
- `author`: ForeignKey(Author)
- `category`: ForeignKey(Category)
- `status`: CharField (choices: draft, published)
- `views`: PositiveIntegerField
- `published_at`: DateTimeField (nullable)
- `created_at`, `updated_at`: DateTimeField

## 🔐 Preparación para Autenticación (Día 4)

El servicio ya incluye:

1. **Middleware `AuthTokenLoggingMiddleware`**: Captura y loguea headers `Authorization`
2. **Esqueleto en OpenAPI**: Definición de `BearerAuth`
3. **ViewSets públicos**: Listos para agregar permisos

### Próximos pasos (Día 4):
- Validar JWT desde Auth Service
- Proteger endpoints de creación/edición
- Enlazar autores con usuarios de Auth

## 📄 Contrato API

El contrato completo de la API está disponible en `openapi.yaml`.

Puedes visualizarlo en [Swagger Editor](https://editor.swagger.io/) o con herramientas locales.

## 🐛 Troubleshooting

### El servicio no inicia

```bash
# Ver logs detallados
docker-compose logs blog

# Verificar que postgres y redis estén healthy
docker-compose ps
```

### Error de conexión a base de datos

```bash
# Verificar variables de entorno
docker-compose config

# Reiniciar postgres
docker-compose restart postgres
```

### Caché no funciona

```bash
# Verificar Redis
docker-compose exec redis redis-cli ping
# Debería responder: PONG

# Ver logs de conexión Redis
docker-compose logs blog | grep -i redis
```

### Si necesitas re-ejecutar el seed

```bash
docker-compose exec blog python manage.py seed_blog
```

### Limpiar y empezar de nuevo

```bash
# Detener servicios
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Esto borra los datos)
docker-compose down -v

# Reconstruir y levantar
docker-compose up -d --build blog
```

## 📚 Recursos

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [django-redis](https://github.com/jazzband/django-redis)
- [OpenAPI Specification](https://swagger.io/specification/)

## ✅ Checklist del Día 3

- [x] Proyecto Django configurado
- [x] Modelos: Category, Author, Post
- [x] Serializers para DRF
- [x] ViewSets con paginación y búsqueda
- [x] Caché Redis en endpoints clave
- [x] Comando seed_blog con datos de ejemplo
- [x] Health check endpoint
- [x] Logging estructurado JSON
- [x] Middleware de request logging
- [x] Middleware para Authorization header
- [x] Dockerfile configurado
- [x] docker-compose.yml actualizado
- [x] OpenAPI contract
- [x] README con documentación completa

## 🎓 Próximos Pasos (Día 4)

1. Integrar autenticación JWT desde Auth Service
2. Proteger endpoints de escritura
3. Enlazar autores con usuarios reales
4. Implementar permisos basados en roles
5. Añadir endpoints POST/PUT/DELETE para posts

---

**Día 3 completado** ✅ | Puerto: **8001** | Documentación: `openapi.yaml`
