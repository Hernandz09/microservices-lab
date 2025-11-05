# Auth Service 🔐

Microservicio de autenticación y gestión de usuarios construido con Django REST Framework y JWT.

## 🎯 Características

- **Registro de usuarios**: Creación de nuevas cuentas
- **Autenticación JWT**: Login con tokens de acceso y refresco
- **Gestión de usuarios**: Modelo de usuario personalizado con email
- **Perfil de usuario**: Endpoint para obtener información del usuario autenticado
- **Integración Redis**: Caché para sesiones y tokens
- **Health Check**: Monitoreo de DB y Redis

## 🏗️ Stack Tecnológico

- **Framework**: Django 5.0 + Django REST Framework 3.15
- **Autenticación**: Simple JWT 5.3
- **Base de datos**: PostgreSQL 15
- **Caché**: Redis 7
- **Servidor**: Gunicorn
- **Containerización**: Docker

## 📦 Estructura del Proyecto

```
auth-service/
├── auth_service/          # Proyecto Django principal
│   ├── settings.py        # Configuración (DB, Redis, JWT, CORS)
│   ├── urls.py           # Rutas principales
│   ├── wsgi.py
│   └── asgi.py
├── users/                 # App de usuarios
│   ├── models.py         # Modelo User personalizado
│   ├── serializers.py    # Serializadores DRF
│   ├── views.py          # Vistas/Endpoints
│   ├── urls.py           # Rutas de la app
│   ├── admin.py          # Configuración del admin
│   └── healthcheck.py    # Health check endpoint
├── Dockerfile
├── requirements.txt
└── manage.py
```

## 🚀 Instalación y Ejecución

### Prerequisitos

- Docker y Docker Compose
- Variables de entorno configuradas en `.env`

### Quick Start

#### 1. Levantar el servicio con Docker Compose

Desde el directorio raíz del proyecto:

```bash
docker-compose up -d auth
```

El servicio estará disponible en: **http://localhost:8000**

#### 2. Verificar que el servicio está funcionando

```bash
# Health check
curl http://localhost:8000/api/health/

# Debería retornar:
# {
#   "status": "healthy",
#   "database": "connected",
#   "redis": "connected"
# }
```

## 🔌 API Endpoints

### Health Check

```bash
GET /api/health/
```

**Respuesta**:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
```

### Registro de Usuario

```bash
POST /api/register/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "mipassword123",
  "password2": "mipassword123",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

**Respuesta (201 Created)**:
```json
{
  "user": {
    "id": 1,
    "email": "usuario@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "date_joined": "2025-11-03T12:00:00Z"
  },
  "message": "Usuario registrado exitosamente"
}
```

### Login (Obtener Tokens)

```bash
POST /api/token/
Content-Type: application/json

{
  "email": "usuario@example.com",
  "password": "mipassword123"
}
```

**Respuesta (200 OK)**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Refrescar Token de Acceso

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Respuesta (200 OK)**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Perfil de Usuario (Autenticado)

```bash
GET /api/me/
Authorization: Bearer {access_token}
```

**Respuesta (200 OK)**:
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "date_joined": "2025-11-03T12:00:00Z"
}
```

## 🧪 Ejemplos con cURL

### Registrar un nuevo usuario

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

### Hacer login

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Obtener perfil (requiere token)

```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### Refrescar token de acceso

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN_HERE"
  }'
```

## 📊 Resumen de Endpoints

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/health/` | Health check (DB + Redis) | No |
| POST | `/api/register/` | Registro de nuevos usuarios | No |
| POST | `/api/token/` | Login - Obtener tokens JWT | No |
| POST | `/api/token/refresh/` | Refrescar access token | No |
| GET | `/api/me/` | Información del usuario autenticado | Sí (Bearer Token) |

## 🔑 Configuración JWT

Los tokens JWT están configurados con los siguientes tiempos de vida:

- **Access Token**: 1 hora
- **Refresh Token**: 1 día

Configuración en `settings.py`:
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## 🗄️ Modelo de Usuario

El servicio usa un modelo de usuario personalizado que extiende `AbstractBaseUser`:

**User Model**:
- `id`: AutoField
- `email`: EmailField (único, usado como USERNAME_FIELD)
- `first_name`: CharField
- `last_name`: CharField
- `is_active`: BooleanField
- `is_staff`: BooleanField
- `is_superuser`: BooleanField
- `date_joined`: DateTimeField

## 🛠️ Comandos Útiles

```bash
# Ver logs
docker-compose logs -f auth

# Ejecutar migraciones
docker-compose exec auth python manage.py migrate

# Crear superusuario para Django Admin
docker-compose exec auth python manage.py createsuperuser

# Shell de Django
docker-compose exec auth python manage.py shell

# Acceder al admin en: http://localhost:8000/admin/

# Entrar al contenedor
docker-compose exec auth bash

# Reiniciar el servicio
docker-compose restart auth

# Reconstruir el contenedor
docker-compose up -d --build auth
```

## 🐛 Troubleshooting

### El servicio no inicia

```bash
# Ver logs detallados
docker-compose logs auth

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

### Token inválido o expirado

Los access tokens expiran después de 1 hora. Usa el refresh token para obtener uno nuevo:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Limpiar y empezar de nuevo

```bash
# Detener servicios
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Esto borra los datos)
docker-compose down -v

# Reconstruir y levantar
docker-compose up -d --build auth
```

## 🔐 Seguridad

### En Producción

Asegúrate de:

1. Cambiar el `SECRET_KEY` en las variables de entorno
2. Configurar `DEBUG=False`
3. Configurar `ALLOWED_HOSTS` correctamente
4. Usar HTTPS
5. Configurar CORS apropiadamente para tu frontend
6. Usar variables de entorno para credenciales sensibles

### CORS

El servicio tiene CORS habilitado para desarrollo. En producción, configura `CORS_ALLOWED_ORIGINS` con las URLs permitidas.

## 📚 Recursos

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decodificar y validar tokens

## 🔗 Integración con Otros Servicios

Este servicio puede ser usado por otros microservicios para:

1. **Validar tokens JWT**: Otros servicios pueden validar el token usando la misma SECRET_KEY
2. **Obtener información del usuario**: Decodificando el token JWT
3. **Implementar autorización**: Basada en roles o permisos del usuario

### Ejemplo de validación de token en otro servicio:

```python
from rest_framework_simplejwt.authentication import JWTAuthentication

class MyProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # request.user estará disponible
        return Response({"message": f"Hello {request.user.email}"})
```

## ✅ Checklist del Día 2

- [x] Código funcional: Microservicio auth-service con Django + JWT
- [x] Modelo User personalizado con email como USERNAME_FIELD
- [x] Endpoints implementados: register, token, token/refresh, me
- [x] Docker funcionando en puerto 8000
- [x] Migraciones aplicadas
- [x] Conexión PostgreSQL configurada
- [x] Conexión Redis configurada
- [x] CORS habilitado
- [x] Health check endpoint
- [x] Documentación completa

---

**Día 2 completado** ✅ | Puerto: **8000** | Autenticación: **JWT**
