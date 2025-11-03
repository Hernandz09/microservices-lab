# Blog Service - Quick Start Guide

Este script te ayudará a levantar y probar el Blog Service.

## Pre-requisitos

Asegúrate de que Docker Desktop esté corriendo.

## Pasos para iniciar

### 1. Levantar servicios (desde el directorio raíz)

```bash
docker-compose up -d blog
```

Esto levantará automáticamente:
- PostgreSQL
- Redis
- Blog Service (con migraciones y seed automático)

### 2. Verificar que todo está funcionando

```bash
# Ver los contenedores corriendo
docker ps

# Deberías ver:
# - db_postgres (healthy)
# - cache_redis (healthy)
# - blog_service (running)
```

### 3. Probar el health check

```bash
curl http://localhost:8001/healthz
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

### 4. Pruebas básicas

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

## Solución de Problemas

### Si el servicio no inicia

```bash
# Ver logs
docker-compose logs blog

# Verificar que postgres está healthy
docker-compose ps

# Reiniciar servicios
docker-compose restart blog
```

### Si necesitas re-ejecutar el seed

```bash
docker-compose exec blog python manage.py seed_blog
```

### Limpiar y empezar de nuevo

```bash
# Detener todo
docker-compose down

# Limpiar volúmenes (¡CUIDADO! Esto borra los datos)
docker-compose down -v

# Levantar de nuevo
docker-compose up -d --build blog
```

## Acceso al Admin de Django

1. Crear un superusuario:
```bash
docker-compose exec blog python manage.py createsuperuser
```

2. Acceder al admin:
```
http://localhost:8001/admin/
```

## Ver logs en tiempo real

```bash
docker-compose logs -f blog
```

## Siguiente Paso

Una vez que todo funcione, continuar con el **Día 4**: Integración JWT entre Auth y Blog Services.
