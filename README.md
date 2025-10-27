# 🚀 Microservices Lab

Laboratorio de arquitectura de microservicios con Django REST Framework, PostgreSQL y Redis.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Servicios](#servicios)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Checklist Día 1](#checklist-día-1)
- [Día 2: Auth Service](#día-2-auth-service)

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React)                    │
└───────────────────┬─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                  Reverse Proxy (Nginx)                   │
└────┬──────────────┬────────────────┬────────────────────┘
     │              │                │
┌────▼────┐   ┌────▼────┐      ┌───▼──────┐
│  Auth   │   │  Blog   │      │  Email   │
│ Service │   │ Service │      │ Service  │
└────┬────┘   └────┬────┘      └──────────┘
     │             │
┌────▼─────────────▼────┐      ┌────────────┐
│   PostgreSQL (DB)      │      │   Redis    │
└────────────────────────┘      └────────────┘
```

### Descripción de Servicios

- **Frontend**: Interfaz de usuario construida con React
- **Reverse Proxy**: Nginx para enrutamiento y balanceo de carga
- **Auth Service**: Gestión de autenticación y autorización de usuarios
- **Blog Service**: CRUD de posts y contenido del blog
- **Email Service**: Envío de notificaciones por correo electrónico
- **PostgreSQL**: Base de datos relacional principal
- **Redis**: Caché en memoria para sesiones y datos temporales

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

## 📦 Instalación

### Prerrequisitos

- Docker Desktop instalado
- Docker Compose v3.9+
- Git

### Configuración Inicial

1. **Clonar el repositorio**

```bash
git clone https://github.com/Hernandz09/microservices-lab.git
cd microservices-lab
```

2. **Configurar variables de entorno**

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus configuraciones personalizadas si es necesario.

3. **Levantar los servicios**

```bash
docker compose up -d
```

4. **Verificar que los contenedores estén corriendo**

```bash
docker ps
```

Deberías ver los contenedores `db_postgres` y `cache_redis` en ejecución.

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
├── docker-compose.yml    ✅ Orquestación de contenedores
├── README.md            ✅ Documentación principal
├── auth-service/        ✅ Estructura creada
├── blog-service/        ✅ Estructura creada
├── email-service/       ✅ Estructura creada
├── frontend/            ✅ Estructura creada
└── reverse-proxy/       ✅ Estructura creada
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

## 📝 Próximos Pasos

- [ ] Implementar el servicio de blog
- [ ] Integrar el servicio de email
- [ ] Desarrollar el frontend
- [ ] Configurar el reverse proxy

## 📄 Licencia

Este proyecto es para fines educativos.

## 👨‍💻 Autor

**Ignacio Hernandez**
- GitHub: [@Hernandz09](https://github.com/Hernandz09)

---

🎓 **Microservices Lab** - Proyecto educativo de arquitectura de microservicios
