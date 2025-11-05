# Email Service 📧

Microservicio de notificaciones y correo electrónico construido con Django REST Framework, Redis y Celery.

## 🎯 Características

- **Formulario de contacto**: Endpoint público para recibir mensajes
- **Notificaciones internas**: Endpoint para comunicación entre microservicios
- **Envío asíncrono**: Cola de emails con Celery + Redis
- **Reintentos automáticos**: 3 intentos con backoff exponencial
- **Idempotencia**: Basada en UUID para evitar duplicados
- **Logs estructurados**: JSON logging para observabilidad
- **Health Check**: Monitoreo de DB, Redis y Celery workers

## 🏗️ Stack Tecnológico

- **Framework**: Django 5.0 + Django REST Framework 3.15
- **Cola de tareas**: Celery 5.4 + Redis 7
- **Base de datos**: PostgreSQL 15
- **Servidor**: Gunicorn
- **Containerización**: Docker

## 📦 Estructura del Proyecto

```
email-service/
├── email_service/          # Proyecto Django principal
│   ├── settings.py        # Configuración (DB, Redis, Celery, Email)
│   ├── urls.py           # Rutas principales
│   ├── celery.py         # Configuración de Celery
│   ├── wsgi.py
│   └── asgi.py
├── notifications/         # App de notificaciones
│   ├── models.py         # ContactMessage, NotificationLog
│   ├── serializers.py    # Serializers DRF
│   ├── views.py          # ContactViewSet, NotifyViewSet
│   ├── tasks.py          # Tareas asíncronas de Celery
│   ├── urls.py
│   └── admin.py
├── utils/                # Utilidades compartidas
│   ├── mailer.py         # Función send_email()
│   ├── logger.py         # JSON formatter
│   ├── middleware.py     # Request logging
│   └── healthcheck.py    # Health check endpoint
├── Dockerfile
├── requirements.txt
├── openapi.yaml         # Contrato API
└── manage.py
```

## 🚀 CÓMO EJECUTAR

### Opción 1: Con Docker Compose (Recomendado)

#### Paso 1: Levantar el servicio

Desde el **directorio raíz del proyecto**:

```bash
# Levantar solo el servicio de email
docker-compose up -d email

# O levantar todos los servicios
docker-compose up -d
```

Esto levantará automáticamente:
- PostgreSQL (compartido)
- Redis (compartido)
- Email Service (puerto 8002)
- Celery Worker (procesamiento asíncrono)

#### Paso 2: Verificar que está funcionando

```bash
# Ver contenedores corriendo
docker ps

# Deberías ver:
# - email_service (puerto 8002)
# - email_worker (Celery)
# - db_postgres (healthy)
# - cache_redis (healthy)

# Verificar health check
curl http://localhost:8002/healthz
```

**Respuesta esperada**:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "celery": "ok"
  }
}
```

#### Paso 3: Ver logs en tiempo real

```bash
# Logs del servicio web
docker-compose logs -f email

# Logs del worker de Celery
docker-compose logs -f email-worker
```

---

### Opción 2: Desarrollo Local (Sin Docker)

#### Requisitos previos:
- Python 3.11+
- PostgreSQL corriendo
- Redis corriendo

#### Paso 1: Crear entorno virtual

```bash
cd email-service
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Paso 2: Instalar dependencias

```bash
pip install -r requirements.txt
```

#### Paso 3: Configurar variables de entorno

Crear archivo `.env` en `email-service/`:

```bash
DEBUG=1
DB_HOST=localhost
DB_NAME=main_db
DB_USER=devuser
DB_PASS=devpass
DB_PORT=5432
REDIS_HOST=localhost
REDIS_PORT=6379
SECRET_KEY=tu-secret-key-aqui
```

#### Paso 4: Aplicar migraciones

```bash
python manage.py migrate
```

#### Paso 5: Ejecutar servidor

```bash
# Terminal 1: Servidor Django
python manage.py runserver 0.0.0.0:8002

# Terminal 2: Celery Worker (en otra terminal)
celery -A email_service worker --loglevel=info
```

---

## 🔌 API Endpoints

### 1. Health Check

```bash
GET /healthz
```

**Ejemplo**:
```bash
curl http://localhost:8002/healthz
```

**Respuesta**:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok",
    "celery": "ok"
  }
}
```

---

### 2. Enviar Formulario de Contacto

```bash
POST /api/contact/
Content-Type: application/json

{
  "name": "Carlos Rivas",
  "email": "carlos@mail.com",
  "message": "Me interesa una colaboración"
}
```

**Ejemplo con cURL**:
```bash
curl -X POST http://localhost:8002/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Rivas",
    "email": "carlos@mail.com",
    "message": "Me interesa una colaboración"
  }'
```

**Respuesta (202 Accepted)**:
```json
{
  "id": 1,
  "status": "queued",
  "message": "Message queued for processing",
  "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

---

### 3. Notificación Interna (Entre Microservicios)

```bash
POST /api/notify/
Content-Type: application/json

{
  "to": "user@mail.com",
  "subject": "Nuevo post publicado",
  "body": "Se ha publicado un nuevo artículo en el blog."
}
```

**Ejemplo con cURL**:
```bash
curl -X POST http://localhost:8002/api/notify/ \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Nuevo post publicado",
    "body": "Se ha publicado un nuevo artículo: Introduction to Microservices"
  }'
```

**Respuesta (202 Accepted)**:
```json
{
  "id": 1,
  "status": "queued",
  "message": "Notification queued for processing",
  "uuid": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
}
```

---

### 4. Listar Mensajes de Contacto

```bash
GET /api/contact/
```

**Ejemplo**:
```bash
curl http://localhost:8002/api/contact/
```

**Respuesta**:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "Carlos Rivas",
      "email": "carlos@mail.com",
      "message": "Me interesa una colaboración",
      "status": "sent",
      "created_at": "2025-11-04T10:30:00Z"
    }
  ]
}
```

---

### 5. Listar Notificaciones

```bash
GET /api/notify/
```

**Ejemplo**:
```bash
curl http://localhost:8002/api/notify/
```

---

## 📊 Resumen de Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/healthz` | Health check (DB + Redis + Celery) | No |
| POST | `/api/contact/` | Enviar mensaje de contacto | No |
| GET | `/api/contact/` | Listar mensajes de contacto | No |
| GET | `/api/contact/{id}/` | Detalle de mensaje | No |
| POST | `/api/notify/` | Enviar notificación interna | No |
| GET | `/api/notify/` | Listar notificaciones | No |
| GET | `/api/notify/{id}/` | Detalle de notificación | No |

---

## 🔄 Celery: Procesamiento Asíncrono

### Tareas Implementadas

#### 1. `send_contact_email_task`
- Envía email cuando se recibe un mensaje de contacto
- **Reintentos**: 3 intentos
- **Delay**: Backoff exponencial (5s, 25s, 125s)
- **Idempotente**: Usa UUID para evitar duplicados

#### 2. `send_notification_task`
- Envía notificaciones entre microservicios
- Mismas características de reintentos

### Monitorear Tareas

```bash
# Ver logs del worker
docker-compose logs -f email-worker

# Entrar al contenedor del worker
docker-compose exec email-worker bash

# Inspeccionar tareas activas (desde dentro del contenedor)
celery -A email_service inspect active
```

---

## 📧 Configuración de Email

### Modo de Desarrollo (Console Backend)

Por defecto, los emails se imprimen en la consola:

```python
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

**Ver emails en logs**:
```bash
docker-compose logs -f email-worker
```

### Modo Archivo (File Backend)

Para guardar emails en archivos:

```python
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "/tmp/sent_emails"
```

```bash
# Ver emails guardados
docker-compose exec email ls -la /tmp/sent_emails/
```

### Modo Producción (SMTP)

Para enviar emails reales, configurar en `.env`:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password
DEFAULT_FROM_EMAIL=noreply@tudominio.com
```

---

## 🗄️ Modelos de Base de Datos

### ContactMessage
- `id`: AutoField
- `uuid`: UUIDField (único, para idempotencia)
- `name`: CharField
- `email`: EmailField
- `message`: TextField
- `status`: CharField (choices: pending, queued, sent, failed)
- `retry_count`: IntegerField
- `error_message`: TextField (nullable)
- `created_at`, `updated_at`: DateTimeField

### NotificationLog
- `id`: AutoField
- `uuid`: UUIDField (único)
- `to`: EmailField
- `subject`: CharField
- `body`: TextField
- `status`: CharField (choices: pending, queued, sent, failed)
- `retry_count`: IntegerField
- `error_message`: TextField (nullable)
- `metadata`: JSONField (datos adicionales)
- `created_at`, `updated_at`: DateTimeField

---

## 🛠️ Comandos Útiles

### Docker Compose

```bash
# Levantar servicios
docker-compose up -d email email-worker

# Ver logs
docker-compose logs -f email
docker-compose logs -f email-worker

# Reiniciar servicios
docker-compose restart email email-worker

# Ejecutar migraciones
docker-compose exec email python manage.py migrate

# Crear superusuario
docker-compose exec email python manage.py createsuperuser

# Shell de Django
docker-compose exec email python manage.py shell

# Acceder al admin: http://localhost:8002/admin/

# Limpiar base de datos
docker-compose exec email python manage.py flush

# Reconstruir contenedores
docker-compose up -d --build email email-worker
```

### Celery

```bash
# Ver tareas activas
docker-compose exec email-worker celery -A email_service inspect active

# Ver tareas registradas
docker-compose exec email-worker celery -A email_service inspect registered

# Ver estadísticas del worker
docker-compose exec email-worker celery -A email_service inspect stats

# Purgar todas las tareas en cola
docker-compose exec email-worker celery -A email_service purge
```

---

## 🧪 Pruebas Completas

### 1. Verificar Health Check

```bash
curl http://localhost:8002/healthz
```

### 2. Enviar Mensaje de Contacto

```bash
curl -X POST http://localhost:8002/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "message": "Este es un mensaje de prueba"
  }'
```

### 3. Ver el Email en Logs

```bash
docker-compose logs -f email-worker
```

Deberías ver algo como:
```
From: noreply@microservices-lab.com
To: test@example.com
Subject: Nuevo mensaje de contacto

Mensaje de: Test User (test@example.com)

Este es un mensaje de prueba
```

### 4. Verificar Estado del Mensaje

```bash
curl http://localhost:8002/api/contact/
```

### 5. Enviar Notificación Interna

```bash
curl -X POST http://localhost:8002/api/notify/ \
  -H "Content-Type: application/json" \
  -d '{
    "to": "admin@example.com",
    "subject": "Test Notification",
    "body": "This is a test notification from the blog service"
  }'
```

### 6. Simular Llamada desde Blog Service

```bash
# Desde dentro del contenedor del blog
docker-compose exec blog bash

# Instalar curl si no está disponible
apt-get update && apt-get install -y curl

# Enviar notificación
curl -X POST http://email:8002/api/notify/ \
  -H "Content-Type: application/json" \
  -d '{
    "to": "subscriber@example.com",
    "subject": "Nuevo post publicado",
    "body": "Se ha publicado: Introduction to Microservices"
  }'
```

---

## 🔍 Observabilidad

### Logs Estructurados

El servicio emite logs en formato JSON:

```json
{
  "timestamp": "2025-11-04T12:00:00.000000",
  "level": "INFO",
  "logger": "email_service",
  "message": "{\"method\": \"POST\", \"path\": \"/api/contact/\", \"status_code\": 202, \"duration_ms\": 45.23}"
}
```

### Healthcheck

El endpoint `/healthz` verifica:
- ✅ Conexión a PostgreSQL
- ✅ Conexión a Redis
- ✅ Workers de Celery activos

### Métricas de Celery

```bash
# Ver estadísticas del worker
docker-compose exec email-worker celery -A email_service inspect stats
```

---

## 🐛 Troubleshooting

### El servicio no inicia

```bash
# Ver logs detallados
docker-compose logs email

# Verificar que postgres y redis estén healthy
docker-compose ps
```

### Celery Worker no procesa tareas

```bash
# Ver logs del worker
docker-compose logs email-worker

# Verificar que Redis esté accesible
docker-compose exec email-worker redis-cli -h redis ping

# Reiniciar worker
docker-compose restart email-worker
```

### Emails no se envían

```bash
# Verificar logs del worker
docker-compose logs -f email-worker

# Verificar estado de las tareas
docker-compose exec email curl http://localhost:8002/api/contact/

# Verificar configuración de email
docker-compose exec email python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

### Limpiar y reiniciar

```bash
# Detener servicios
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Borra datos)
docker-compose down -v

# Reconstruir y levantar
docker-compose up -d --build email email-worker
```

---

## 🔐 Seguridad

### En Producción

1. **Variables de entorno**: Nunca hardcodear credenciales
2. **CORS**: Configurar `CORS_ALLOWED_ORIGINS` apropiadamente
3. **Rate Limiting**: Implementar throttling en DRF
4. **Autenticación**: Proteger endpoints internos con tokens
5. **HTTPS**: Usar certificados SSL/TLS
6. **Secrets**: Usar servicios como AWS Secrets Manager

---

## 🔗 Integración con Otros Servicios

### Desde Blog Service

```python
import requests

# Notificar cuando se publica un post
def notify_new_post(post):
    payload = {
        "to": "subscribers@example.com",
        "subject": f"Nuevo post: {post.title}",
        "body": f"{post.title}\n\n{post.excerpt}"
    }
    
    try:
        response = requests.post(
            "http://email:8002/api/notify/",
            json=payload,
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
```

### Desde Auth Service

```python
# Notificar cuando se registra un usuario
def notify_new_user(user):
    payload = {
        "to": user.email,
        "subject": "Bienvenido a Microservices Lab",
        "body": f"Hola {user.first_name}, gracias por registrarte!"
    }
    
    requests.post("http://email:8002/api/notify/", json=payload)
```

---

## 📚 Recursos

- [Django Documentation](https://docs.djangoproject.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Redis](https://redis.io/documentation)

---

## ✅ Checklist del Día 4

- [x] Microservicio Email funcional en puerto 8002
- [x] POST /api/contact/ almacena y encola mensajes
- [x] POST /api/notify/ para comunicación entre servicios
- [x] Celery + Redis para procesamiento asíncrono
- [x] Reintentos automáticos (3 intentos con backoff)
- [x] Idempotencia basada en UUID
- [x] Health check completo (/healthz)
- [x] Logs estructurados en JSON
- [x] Modelos: ContactMessage y NotificationLog
- [x] Docker + docker-compose configurado
- [x] OpenAPI contract documentado
- [x] README con ejemplos completos

---

## 🎓 Próximos Pasos (Día 5)

1. Implementar autenticación en endpoints internos
2. Añadir rate limiting
3. Implementar templates HTML para emails
4. Integrar con servicio de email real (SendGrid, SES)
5. Añadir métricas con Prometheus
6. Implementar circuit breaker para resiliencia

---

**Día 4 completado** ✅ | Puerto: **8002** | Procesamiento: **Asíncrono con Celery**
