import psycopg2
import redis
import os

# Variables de entorno (en producción vienen del .env)
POSTGRES_USER = os.getenv("POSTGRES_USER", "devuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "devpass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "main_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")  # Nombre del servicio en Docker
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print("Probando conexión a PostgreSQL...")
try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=5432
    )
    print("✅ Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print("❌ Error PostgreSQL:", e)

print("\nProbando conexión a Redis...")
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    r.set("test", "ok")
    print("✅ Conexión exitosa a Redis:", r.get("test"))
except Exception as e:
    print("❌ Error Redis:", e)
