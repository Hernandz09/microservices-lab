# 🚀 Microservices Lab

Laboratorio de arquitectura de microservicios con FastAPI, PostgreSQL y Redis.

## 📋 Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Servicios](#servicios)
- [Tecnologías](#tecnologías)
- [Instalación](#instalación)
- [Uso](#uso)
- [Checklist Día 1](#checklist-día-1)

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
| Backend | FastAPI | 0.x |
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
- [ ] **Captura o video corto**: Mostrando los contenedores en ejecución (`docker ps`)

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

## 📝 Próximos Pasos

- [ ] Implementar el servicio de autenticación
- [ ] Configurar el servicio de blog
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
