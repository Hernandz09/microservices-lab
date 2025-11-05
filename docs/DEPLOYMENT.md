# 🚀 Guía de Deployment

Guía completa para desplegar Microservices Lab en diferentes entornos.

## 📋 Tabla de Contenidos

- [Desarrollo Local](#desarrollo-local)
- [Docker Compose (Staging)](#docker-compose-staging)
- [Producción - Cloud](#producción---cloud)
  - [AWS ECS](#aws-ecs)
  - [Google Cloud Run](#google-cloud-run)
  - [Azure Container Apps](#azure-container-apps)
- [Kubernetes](#kubernetes)
- [Variables de Entorno](#variables-de-entorno)
- [Backups](#backups)
- [Rollback](#rollback)

---

## 🏠 Desarrollo Local

### Con Docker Compose

```bash
# Clonar repositorio
git clone https://github.com/Hernandz09/microservices-lab.git
cd microservices-lab

# Configurar variables
cp .env.example .env

# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f
```

### Sin Docker (Django local)

```bash
# Instalar Python 3.11+
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Servicio Auth
cd auth-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

# En otra terminal - Servicio Blog
cd blog-service
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_blog
python manage.py runserver 8001
```

---

## 🐳 Docker Compose (Staging)

Entorno de staging similar a producción.

### docker-compose.prod.yml

```yaml
services:
  postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./backups:/backups
    networks:
      - backend

  redis:
    image: redis:7
    restart: always
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redisdata:/data
    networks:
      - backend

  auth:
    build: 
      context: ./auth-service
      dockerfile: Dockerfile.prod
    restart: always
    environment:
      - DEBUG=0
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
    depends_on:
      - postgres
      - redis
    networks:
      - backend
      - frontend

  blog:
    build: 
      context: ./blog-service
      dockerfile: Dockerfile.prod
    restart: always
    environment:
      - DEBUG=0
    depends_on:
      - postgres
      - redis
    networks:
      - backend
      - frontend

  email:
    build: 
      context: ./email-service
      dockerfile: Dockerfile.prod
    restart: always
    depends_on:
      - postgres
      - redis
    networks:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./reverse-proxy/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./reverse-proxy/ssl:/etc/nginx/ssl:ro
      - static_volume:/app/staticfiles
    depends_on:
      - auth
      - blog
      - email
    networks:
      - frontend

volumes:
  pgdata:
  redisdata:
  static_volume:

networks:
  frontend:
  backend:
```

### Desplegar

```bash
# Construir imágenes
docker compose -f docker-compose.prod.yml build

# Levantar en modo detached
docker compose -f docker-compose.prod.yml up -d

# Migrar base de datos
docker compose -f docker-compose.prod.yml exec auth python manage.py migrate
docker compose -f docker-compose.prod.yml exec blog python manage.py migrate

# Recolectar archivos estáticos
docker compose -f docker-compose.prod.yml exec auth python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml exec blog python manage.py collectstatic --noinput
```

---

## ☁️ Producción - Cloud

### AWS ECS (Elastic Container Service)

#### 1. Preparar imágenes Docker

```bash
# Construir y tagear imágenes
docker build -t auth-service:latest ./auth-service
docker build -t blog-service:latest ./blog-service
docker build -t email-service:latest ./email-service

# Login a ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Crear repositorios ECR
aws ecr create-repository --repository-name auth-service
aws ecr create-repository --repository-name blog-service
aws ecr create-repository --repository-name email-service

# Push a ECR
docker tag auth-service:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/auth-service:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/auth-service:latest
```

#### 2. Crear RDS y ElastiCache

```bash
# PostgreSQL RDS
aws rds create-db-instance \
  --db-instance-identifier microservices-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20

# Redis ElastiCache
aws elasticache create-cache-cluster \
  --cache-cluster-id microservices-cache \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

#### 3. Crear Task Definition y Service

Ver `deploy/aws/task-definition.json`

```bash
# Crear cluster
aws ecs create-cluster --cluster-name microservices-cluster

# Registrar task definition
aws ecs register-task-definition --cli-input-json file://deploy/aws/task-definition.json

# Crear service
aws ecs create-service \
  --cluster microservices-cluster \
  --service-name auth-service \
  --task-definition auth-service:1 \
  --desired-count 2 \
  --launch-type FARGATE
```

---

### Google Cloud Run

```bash
# Autenticar
gcloud auth login

# Configurar proyecto
gcloud config set project YOUR_PROJECT_ID

# Build y deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/auth-service ./auth-service
gcloud run deploy auth-service \
  --image gcr.io/YOUR_PROJECT_ID/auth-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DB_HOST=10.0.0.1,DB_NAME=main_db"

# Cloud SQL (PostgreSQL)
gcloud sql instances create microservices-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Memorystore (Redis)
gcloud redis instances create microservices-cache \
  --size=1 \
  --region=us-central1
```

---

### Azure Container Apps

```bash
# Login
az login

# Crear resource group
az group create --name microservices-rg --location eastus

# Crear Container Apps environment
az containerapp env create \
  --name microservices-env \
  --resource-group microservices-rg \
  --location eastus

# Deploy auth service
az containerapp create \
  --name auth-service \
  --resource-group microservices-rg \
  --environment microservices-env \
  --image youracr.azurecr.io/auth-service:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars DB_HOST=postgres.database.azure.com

# Azure Database for PostgreSQL
az postgres server create \
  --resource-group microservices-rg \
  --name microservices-db \
  --location eastus \
  --sku-name B_Gen5_1

# Azure Cache for Redis
az redis create \
  --resource-group microservices-rg \
  --name microservices-cache \
  --location eastus \
  --sku Basic \
  --vm-size c0
```

---

## ☸️ Kubernetes

### Estructura de archivos

```
k8s/
├── namespace.yaml
├── postgres/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── pvc.yaml
├── redis/
│   ├── deployment.yaml
│   └── service.yaml
├── auth-service/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── blog-service/
│   └── ...
└── email-service/
    └── ...
```

### Deploy en Kubernetes

```bash
# Crear namespace
kubectl create namespace microservices

# Aplicar secrets
kubectl create secret generic db-credentials \
  --from-literal=username=devuser \
  --from-literal=password=devpass \
  -n microservices

# Aplicar configuraciones
kubectl apply -f k8s/ -n microservices

# Ver pods
kubectl get pods -n microservices

# Ver logs
kubectl logs -f deployment/auth-service -n microservices

# Escalar servicio
kubectl scale deployment auth-service --replicas=5 -n microservices
```

### Helm Chart (Recomendado)

```bash
# Instalar con Helm
helm install microservices ./helm/microservices-lab \
  --namespace microservices \
  --create-namespace \
  --set postgres.password=YOUR_PASSWORD
```

---

## 🔐 Variables de Entorno

### Producción

Nunca uses los valores de `.env.example` en producción.

**Generación segura**:

```bash
# Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Passwords seguros
openssl rand -base64 32
```

### Gestión de Secrets

**AWS Secrets Manager**:
```bash
aws secretsmanager create-secret \
  --name microservices/db \
  --secret-string '{"username":"admin","password":"SECURE_PASSWORD"}'
```

**Google Secret Manager**:
```bash
echo -n "SECURE_PASSWORD" | gcloud secrets create db-password --data-file=-
```

**Kubernetes Secrets**:
```bash
kubectl create secret generic app-secrets \
  --from-literal=db-password=SECURE_PASSWORD \
  --from-literal=secret-key=DJANGO_SECRET_KEY
```

---

## 💾 Backups

### PostgreSQL

**Backup manual**:
```bash
# Desde contenedor
docker exec db_postgres pg_dump -U devuser main_db > backup_$(date +%Y%m%d).sql

# Restaurar
docker exec -i db_postgres psql -U devuser main_db < backup_20251104.sql
```

**Backup automático (cron)**:
```bash
# Agregar a crontab
0 2 * * * docker exec db_postgres pg_dump -U devuser main_db | gzip > /backups/db_$(date +\%Y\%m\%d).sql.gz
```

### Redis

**AOF (Append Only File)**:
```bash
# En docker-compose.yml
redis:
  command: redis-server --appendonly yes
  volumes:
    - ./redis-data:/data

# Backup
docker exec cache_redis redis-cli BGSAVE
```

---

## ⏪ Rollback

### Docker Compose

```bash
# Ver historial de imágenes
docker images auth-service

# Rollback a versión anterior
docker tag auth-service:v1.2 auth-service:latest
docker compose up -d auth

# O usar imagen específica
docker compose -f docker-compose.prod.yml up -d --no-deps auth
```

### Kubernetes

```bash
# Ver historial de deployments
kubectl rollout history deployment/auth-service -n microservices

# Rollback a revisión anterior
kubectl rollout undo deployment/auth-service -n microservices

# Rollback a revisión específica
kubectl rollout undo deployment/auth-service --to-revision=2 -n microservices
```

### AWS ECS

```bash
# Listar task definitions
aws ecs list-task-definitions --family-prefix auth-service

# Actualizar servicio a versión anterior
aws ecs update-service \
  --cluster microservices-cluster \
  --service auth-service \
  --task-definition auth-service:1
```

---

## 📊 Monitoreo

### Health Checks

```bash
# Verificar salud de servicios
curl http://your-domain.com/api/auth/health
curl http://your-domain.com/api/blog/healthz
curl http://your-domain.com/api/email/healthz
```

### Prometheus + Grafana (Futuro)

```yaml
# docker-compose.monitoring.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

grafana:
  image: grafana/grafana
  ports:
    - "3000:3000"
```

---

## 🚨 Troubleshooting

### Contenedor no inicia

```bash
# Ver logs detallados
docker logs auth_service --tail 100

# Inspeccionar contenedor
docker inspect auth_service

# Entrar al contenedor
docker exec -it auth_service /bin/bash
```

### Conexión a DB falla

```bash
# Verificar conectividad
docker exec auth_service ping postgres

# Test de conexión PostgreSQL
docker exec auth_service python manage.py dbshell
```

### Redis no conecta

```bash
# Test de Redis
docker exec cache_redis redis-cli ping

# Ver configuración
docker exec cache_redis redis-cli CONFIG GET requirepass
```

---

## 📚 Referencias

- [Docker Compose Production](https://docs.docker.com/compose/production/)
- [AWS ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [Kubernetes Django](https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/)
- [12-Factor App](https://12factor.net/)

---

💡 **Tip**: Siempre prueba en staging antes de desplegar a producción.
