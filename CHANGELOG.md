# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planeado
- Integración JWT entre servicios
- Endpoints protegidos (POST/PUT/DELETE)
- Frontend React
- Reverse Proxy Nginx
- CI/CD con GitHub Actions
- Tests automatizados end-to-end
- Documentación Swagger UI

---

## [0.3.0] - 2025-11-04

### Agregado
- 📧 **Email Service**: Servicio completo de notificaciones
  - Envío asíncrono con Celery
  - Worker para procesamiento en background
  - Modelos de notificaciones
  - Health check endpoint
- 📚 **Documentación mejorada**:
  - README.md completo con badges
  - ARCHITECTURE.md con diagramas detallados
  - DEPLOYMENT.md con guías de despliegue
  - CONTRIBUTING.md con guías de contribución
  - READMEs en frontend/ y reverse-proxy/
- 📄 **Archivos de proyecto**:
  - LICENSE (MIT)
  - .gitattributes para normalización
  - .env.example mejorado
  - CHANGELOG.md
- 🐳 **Docker**: Celery worker en docker-compose

### Cambiado
- README.md reorganizado con mejor estructura
- Documentación histórica movida a secciones colapsables

---

## [0.2.0] - 2025-10-27

### Agregado
- 📝 **Blog Service**: Microservicio completo de blog
  - Modelos: Category, Author, Post
  - Endpoints públicos GET
  - Búsqueda full-text en posts
  - Paginación (10 items/página)
  - Caché Redis con TTL
  - Contador de vistas automático
  - Comando seed_blog con 30 posts
  - Health check endpoint
  - Logging estructurado en JSON
  - Middleware de logging
  - OpenAPI contract completo
- 📊 **Datos de ejemplo**: 5 categorías, 3 autores, 30 posts
- 🔧 **Optimizaciones**:
  - Cache de categorías (60s TTL)
  - Cache de posts (120s TTL)

### Cambiado
- docker-compose.yml actualizado con blog service
- README.md con documentación del Blog Service

---

## [0.1.0] - 2025-10-26

### Agregado
- 🔐 **Auth Service**: Microservicio de autenticación
  - Modelo User personalizado con email
  - Endpoint de registro (`/api/register/`)
  - Login con JWT (`/api/token/`)
  - Refresh token (`/api/token/refresh/`)
  - Perfil autenticado (`/api/me/`)
  - Configuración de CORS
  - Health check
- 🐳 **Infraestructura base**:
  - PostgreSQL 15
  - Redis 7
  - docker-compose.yml funcional
- 📦 **Dependencias**:
  - Django 5.0
  - Django REST Framework
  - SimpleJWT para tokens
  - psycopg2 para PostgreSQL
- 📚 **Documentación**:
  - README.md inicial
  - Arquitectura del sistema
  - Capturas de pantalla
  - Colección Postman

### Configuración Inicial
- Repositorio Git
- .gitignore completo
- .env para variables de entorno
- Estructura de carpetas por servicio

---

## [0.0.1] - 2025-10-25

### Agregado
- 🎉 Inicio del proyecto
- 📋 Planificación de arquitectura de microservicios
- 🐳 Configuración inicial de Docker
- 📖 README básico

---

## Tipos de Cambios

- **Agregado** (`Added`): Para nuevas funcionalidades
- **Cambiado** (`Changed`): Para cambios en funcionalidades existentes
- **Deprecado** (`Deprecated`): Para funcionalidades que serán eliminadas
- **Eliminado** (`Removed`): Para funcionalidades eliminadas
- **Corregido** (`Fixed`): Para corrección de bugs
- **Seguridad** (`Security`): Para vulnerabilidades de seguridad

---

[Unreleased]: https://github.com/Hernandz09/microservices-lab/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Hernandz09/microservices-lab/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Hernandz09/microservices-lab/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Hernandz09/microservices-lab/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/Hernandz09/microservices-lab/releases/tag/v0.0.1
