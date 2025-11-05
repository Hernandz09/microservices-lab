# 🏗️ Arquitectura del Sistema

## Visión General

Microservices Lab es una aplicación distribuida basada en microservicios que implementa un sistema de blog con autenticación JWT y notificaciones por email.

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│                   Port: 3000 (futuro)                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              Reverse Proxy (Nginx)                          │
│                   Port: 80 (futuro)                         │
└────┬──────────────┬────────────────┬────────────────────────┘
     │              │                │
┌────▼────┐   ┌────▼────┐      ┌───▼──────┐
│  Auth   │   │  Blog   │      │  Email   │
│ Service │   │ Service │      │ Service  │
│  :8000  │   │  :8001  │      │  :8002   │
└────┬────┘   └────┬────┘      └────┬─────┘
     │             │                 │
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

## Componentes

### 1. Frontend (Futuro)
**Stack**: React + Vite
**Responsabilidades**:
- Interfaz de usuario
- Consumo de APIs REST
- Gestión de estado (Redux/Zustand)
- Autenticación con tokens JWT

### 2. Reverse Proxy (Futuro)
**Stack**: Nginx
**Responsabilidades**:
- Enrutamiento de peticiones
- Load balancing
- SSL/TLS termination
- Static file serving
- Rate limiting

**Configuración de rutas**:
```nginx
/api/auth/*   → auth-service:8000
/api/blog/*   → blog-service:8001
/api/email/*  → email-service:8002
/*            → frontend:3000
```

### 3. Auth Service
**Stack**: Django 5.0 + DRF + SimpleJWT
**Puerto**: 8000
**Base de datos**: PostgreSQL (shared)
**Cache**: Redis (shared)

**Responsabilidades**:
- Registro de usuarios
- Autenticación (JWT)
- Gestión de tokens (access/refresh)
- Perfil de usuario
- Roles y permisos (futuro)

**Endpoints**:
- `POST /api/register/` - Registro
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token
- `GET /api/me/` - Perfil autenticado

**Modelo de datos**:
```python
User:
  - id (UUID)
  - email (unique)
  - password (hashed)
  - first_name
  - last_name
  - is_active
  - date_joined
```

### 4. Blog Service
**Stack**: Django 5.0 + DRF
**Puerto**: 8001
**Base de datos**: PostgreSQL (shared)
**Cache**: Redis (shared)

**Responsabilidades**:
- CRUD de posts
- Gestión de categorías
- Gestión de autores
- Búsqueda y filtrado
- Sistema de caché
- Contador de vistas

**Endpoints**:
- `GET /api/categories/` - Listar categorías (cached 60s)
- `GET /api/posts/` - Listar posts (paginado)
- `GET /api/posts?search=query` - Buscar posts
- `GET /api/posts/{slug}/` - Detalle de post (cached 120s)
- `POST /api/posts/` - Crear post (autenticado) [futuro]
- `PUT /api/posts/{slug}/` - Actualizar post (autenticado) [futuro]
- `DELETE /api/posts/{slug}/` - Eliminar post (autenticado) [futuro]

**Modelos de datos**:
```python
Category:
  - id
  - name (unique)
  - slug (auto)
  - is_active

Author:
  - id
  - display_name
  - email (unique)
  - bio
  - is_active

Post:
  - id
  - title
  - slug (auto)
  - body
  - excerpt (auto)
  - author (FK → Author)
  - category (FK → Category)
  - status (draft/published)
  - views (counter)
  - published_at
```

### 5. Email Service
**Stack**: Django 5.0 + DRF + Celery
**Puerto**: 8002
**Base de datos**: PostgreSQL (shared)
**Queue**: Redis (Celery broker)

**Responsabilidades**:
- Envío de emails asíncrono
- Templates de email
- Cola de notificaciones
- Tracking de emails enviados

**Endpoints**:
- `POST /api/send/` - Enviar email (asíncrono)
- `GET /api/notifications/` - Historial de notificaciones

**Workers**:
- `celery_worker`: Procesa tareas en background
  - Queue: `emails`, `notifications`

**Modelos de datos**:
```python
Notification:
  - id
  - email_to
  - subject
  - body
  - status (pending/sent/failed)
  - sent_at
  - created_at
```

### 6. PostgreSQL
**Versión**: 15
**Puerto**: 5432

**Base de datos compartida**: `main_db`

**Tablas por servicio**:
```
auth_service:
  - users_user

blog_service:
  - categories_category
  - authors_author
  - posts_post

email_service:
  - notifications_notification
```

**Ventajas de DB compartida**:
- Simplifica transacciones entre servicios
- Menor overhead operacional
- Mejor para proyectos educativos/pequeños

**Desventajas**:
- Acoplamiento de datos
- Escalado más complejo

> **Nota**: En producción se recomienda DB por servicio.

### 7. Redis
**Versión**: 7
**Puerto**: 6379

**Usos**:
1. **Cache** (auth + blog):
   - Categorías: 60s TTL
   - Posts detalle: 120s TTL
   - Sesiones de usuario (futuro)

2. **Message Broker** (email):
   - Cola de Celery
   - Tareas asíncronas

**Estructura de keys**:
```
# Cache
cache:categories:all
cache:post:{slug}

# Celery
celery:task:{task_id}
```

## Patrones de Diseño

### 1. API Gateway (Futuro con Nginx)
Punto único de entrada para clientes.

### 2. Database per Service (Parcial)
Cada servicio tiene sus propias tablas en DB compartida.

### 3. Asynchronous Messaging
Email service usa Celery + Redis para procesamiento asíncrono.

### 4. Cache-Aside Pattern
Blog service implementa cache con invalidación por TTL.

### 5. JWT Authentication
Auth service genera tokens que otros servicios validan.

## Flujos de Datos

### Flujo de Autenticación

```
1. Usuario → Frontend → POST /api/auth/register/
2. Auth Service → PostgreSQL (crear usuario)
3. Auth Service → Frontend (respuesta 201)

4. Usuario → Frontend → POST /api/auth/token/
5. Auth Service → PostgreSQL (verificar credenciales)
6. Auth Service → Frontend (tokens JWT)

7. Frontend guarda tokens en localStorage
8. Frontend incluye token en header: Authorization: Bearer {access_token}
```

### Flujo de Lectura de Posts

```
1. Usuario → Frontend → GET /api/blog/posts/

2. Blog Service verifica cache Redis
   ├─ Cache hit → devolver desde Redis
   └─ Cache miss → consultar PostgreSQL
                 → guardar en Redis (TTL)
                 → devolver datos

3. Blog Service → Frontend (JSON response)
```

### Flujo de Creación de Post (Futuro)

```
1. Usuario → Frontend → POST /api/blog/posts/
   Headers: Authorization: Bearer {token}

2. Blog Service → Auth Service (validar JWT)
   └─ Opción A: Request HTTP a /api/auth/verify/
   └─ Opción B: Validar firma JWT localmente (shared secret)

3. Auth Service → Blog Service (user_id + permisos)

4. Blog Service → PostgreSQL (crear post)

5. Blog Service → Email Service (notificación)
   POST /api/email/send/
   {
     "template": "new_post",
     "to": "admin@example.com",
     "context": { "post_title": "..." }
   }

6. Email Service → Celery/Redis (encolar tarea)

7. Celery Worker → SMTP Server (enviar email)

8. Blog Service → Redis (invalidar cache)

9. Blog Service → Frontend (respuesta 201)
```

## Comunicación entre Servicios

### Sincrónica (HTTP REST)
- Blog → Auth: Validar JWT
- Frontend → Todos: Operaciones CRUD

### Asincrónica (Message Queue)
- Blog → Email: Notificación de nuevo post
- Email → SMTP: Envío real de emails

### Shared Database (Actual)
- Todos los servicios → PostgreSQL compartido

## Seguridad

### Autenticación
- JWT con access token (corta duración) + refresh token
- Tokens firmados con HS256 (shared secret)
- Password hashing con Django's PBKDF2

### Autorización (Futuro)
- Roles: Admin, Editor, Reader
- Permisos en cada endpoint
- Validación en cada servicio

### CORS
- Configurado en cada servicio
- Whitelist de orígenes permitidos

### Secrets Management
- Variables de entorno (`.env`)
- No commitear secrets en Git
- Usar Docker secrets en producción

### Network Security
- Servicios en red privada Docker
- Solo puertos necesarios expuestos
- Rate limiting en Nginx (futuro)

## Escalabilidad

### Horizontal Scaling

**Fácil de escalar**:
- Frontend (stateless)
- Todos los servicios Django (stateless con session en Redis)

**Configuración ejemplo**:
```yaml
# docker-compose.yml
auth:
  deploy:
    replicas: 3
  
blog:
  deploy:
    replicas: 5  # Servicio más demandado
```

**Requiere configuración**:
- PostgreSQL (replicación master-slave)
- Redis (cluster mode)

### Vertical Scaling

Aumentar recursos de contenedores:
```yaml
auth:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
```

### Caching Strategy

1. **Application-level** (implementado):
   - Redis cache en Blog Service
   - TTL corto para datos volátiles

2. **Database-level** (futuro):
   - Query caching en PostgreSQL
   - Materialized views

3. **CDN** (futuro):
   - Cloudflare para static assets
   - Cache de endpoints públicos

## Monitoreo y Logging

### Logs Estructurados
- Formato JSON en cada servicio
- Middleware de logging
- Request ID para tracing

**Ejemplo**:
```json
{
  "timestamp": "2025-11-04T10:30:00Z",
  "service": "blog-service",
  "level": "INFO",
  "method": "GET",
  "path": "/api/posts/",
  "status": 200,
  "duration_ms": 45,
  "user_id": "uuid-here"
}
```

### Health Checks
- Cada servicio expone `/healthz`
- Verifica DB + Redis connectivity
- Docker healthcheck configurado

### Métricas (Futuro)
- Prometheus para recolección
- Grafana para visualización
- Alertas en Slack/Email

## Deployment

### Desarrollo (Actual)
```bash
docker compose up -d
```

### Producción (Futuro)

**Opción 1: Docker Swarm**
```bash
docker stack deploy -c docker-stack.yml microservices
```

**Opción 2: Kubernetes**
```bash
kubectl apply -f k8s/
```

**Opción 3: Cloud (AWS ECS/GCP Cloud Run)**
- Cada servicio en contenedor
- Managed PostgreSQL (RDS/Cloud SQL)
- Managed Redis (ElastiCache/Memorystore)

## Consideraciones de Producción

### Pendientes
- [ ] HTTPS en Nginx
- [ ] Database backups automáticos
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring y alerting
- [ ] Rate limiting
- [ ] Database por servicio
- [ ] Service mesh (Istio/Linkerd)
- [ ] API versioning
- [ ] Documentación Swagger UI
- [ ] Tests end-to-end automatizados

---

📚 **Referencias**:
- [Microservices Patterns](https://microservices.io/patterns/index.html)
- [12-Factor App](https://12factor.net/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
