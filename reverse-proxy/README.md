# 🔀 Reverse Proxy (Nginx)

> 📋 **Estado**: Pendiente de implementación

Nginx como API Gateway y reverse proxy para enrutar peticiones a los microservicios.

## 🎯 Objetivos

- Punto único de entrada (API Gateway)
- Enrutamiento de peticiones a servicios backend
- Load balancing
- SSL/TLS termination
- Servir archivos estáticos del frontend
- Rate limiting y protección DDoS
- Compresión gzip

## 🏗️ Arquitectura

```
                    ┌──────────────┐
                    │   Client     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │    Nginx     │  :80, :443
                    │ Reverse Proxy│
                    └──────┬───────┘
                           │
        ┏━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┓
        ▼                  ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Auth Service  │  │ Blog Service  │  │ Email Service │
│    :8000      │  │    :8001      │  │    :8002      │
└───────────────┘  └───────────────┘  └───────────────┘
```

## 📁 Estructura de Archivos

```
reverse-proxy/
├── nginx.conf              # Configuración principal
├── conf.d/
│   ├── auth-service.conf   # Config de auth
│   ├── blog-service.conf   # Config de blog
│   ├── email-service.conf  # Config de email
│   └── frontend.conf       # Config de frontend
├── ssl/
│   ├── cert.pem           # Certificado SSL
│   └── key.pem            # Llave privada
├── templates/
│   └── default.conf.template
├── Dockerfile
└── README.md
```

## ⚙️ Configuración

### nginx.conf (Principal)

```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    log_format json escape=json '{'
        '"time":"$time_iso8601",'
        '"remote_addr":"$remote_addr",'
        '"request_method":"$request_method",'
        '"request_uri":"$request_uri",'
        '"status":$status,'
        '"body_bytes_sent":$body_bytes_sent,'
        '"request_time":$request_time,'
        '"upstream_addr":"$upstream_addr",'
        '"upstream_response_time":"$upstream_response_time"'
    '}';

    access_log /var/log/nginx/access.log json;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;

    # Upstream definitions
    upstream auth_backend {
        least_conn;
        server auth:8000 max_fails=3 fail_timeout=30s;
        # server auth2:8000 max_fails=3 fail_timeout=30s;  # For scaling
    }

    upstream blog_backend {
        least_conn;
        server blog:8001 max_fails=3 fail_timeout=30s;
    }

    upstream email_backend {
        least_conn;
        server email:8002 max_fails=3 fail_timeout=30s;
    }

    # Include service configurations
    include /etc/nginx/conf.d/*.conf;
}
```

### conf.d/default.conf

```nginx
server {
    listen 80;
    server_name localhost;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # Max upload size
    client_max_body_size 10M;

    # Frontend (React)
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # Auth Service
    location /api/auth/ {
        limit_req zone=auth_limit burst=20 nodelay;
        
        proxy_pass http://auth_backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Blog Service
    location /api/blog/ {
        limit_req zone=api_limit burst=30 nodelay;
        
        proxy_pass http://blog_backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Cache static content
        proxy_cache_bypass $http_upgrade;
    }

    # Email Service
    location /api/email/ {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://email_backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
}

# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name localhost;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Same configuration as port 80
    include /etc/nginx/conf.d/locations.conf;
}
```

## 🐳 Dockerfile

```dockerfile
FROM nginx:alpine

# Copiar configuraciones
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Crear directorio para SSL (opcional)
RUN mkdir -p /etc/nginx/ssl

# Exponer puertos
EXPOSE 80 443

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

## 🚀 Uso

### Desarrollo Local

```bash
# Build imagen
docker build -t reverse-proxy:latest .

# Run con docker compose
docker compose up -d nginx

# Ver logs
docker logs -f reverse_proxy
```

### Generar Certificados SSL (Self-signed para desarrollo)

```bash
# Crear directorio
mkdir -p ssl

# Generar certificado auto-firmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

### Producción con Let's Encrypt

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renovación
sudo certbot renew --dry-run
```

## 🔧 Load Balancing

Para escalar horizontalmente:

```nginx
upstream auth_backend {
    least_conn;  # o ip_hash, random, round_robin
    
    server auth1:8000 weight=3;
    server auth2:8000 weight=2;
    server auth3:8000 weight=1 backup;
    
    # Health checks
    keepalive 32;
}
```

## 🛡️ Seguridad

### Rate Limiting

```nginx
# Configuración global
http {
    # API endpoints
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
    
    # Login endpoint (más restrictivo)
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
}

# Aplicar en location
location /api/auth/token/ {
    limit_req zone=login burst=3 nodelay;
    limit_req_status 429;
    # ...
}
```

### IP Blacklist/Whitelist

```nginx
# Bloquear IPs específicas
location /admin {
    deny 192.168.1.100;
    deny 10.0.0.0/8;
    allow all;
}

# Permitir solo IPs específicas
location /api/internal/ {
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
}
```

### Protección DDoS básica

```nginx
# Límites de conexiones
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

location / {
    limit_conn conn_limit 10;  # Max 10 conexiones simultáneas por IP
}
```

## 📊 Monitoreo

### Nginx Stub Status

```nginx
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

### Prometheus Exporter

```yaml
# docker-compose.yml
nginx-exporter:
  image: nginx/nginx-prometheus-exporter
  command:
    - -nginx.scrape-uri=http://nginx/nginx_status
  ports:
    - "9113:9113"
```

## 🧪 Testing

```bash
# Test de configuración
docker exec reverse_proxy nginx -t

# Reload sin downtime
docker exec reverse_proxy nginx -s reload

# Ver configuración activa
docker exec reverse_proxy cat /etc/nginx/nginx.conf
```

## 🔗 Integración en docker-compose.yml

```yaml
services:
  nginx:
    build: ./reverse-proxy
    container_name: reverse_proxy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./reverse-proxy/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./reverse-proxy/conf.d:/etc/nginx/conf.d:ro
      - ./reverse-proxy/ssl:/etc/nginx/ssl:ro
      - static_volume:/app/staticfiles:ro
      - media_volume:/app/media:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - auth
      - blog
      - email
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3

volumes:
  static_volume:
  media_volume:

networks:
  frontend:
  backend:
```

## 📚 Referencias

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Rate Limiting](https://www.nginx.com/blog/rate-limiting-nginx/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)

---

📌 **Nota**: Este servicio está pendiente de implementación. La configuración es una propuesta inicial lista para usar.
