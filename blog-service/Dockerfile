FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto 8001
EXPOSE 8001

# Comando por defecto
CMD ["gunicorn", "blog_service.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3", "--reload"]
