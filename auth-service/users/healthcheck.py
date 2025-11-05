"""
Healthcheck endpoint para Auth Service
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def healthcheck(request):
    """
    Endpoint de healthcheck que verifica:
    - Conexión a PostgreSQL
    - Conexión a Redis
    """
    health_data = {
        'status': 'healthy',
        'service': 'auth',
        'database': 'unknown',
        'redis': 'unknown',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_data['database'] = 'connected'
    except Exception as e:
        health_data['status'] = 'unhealthy'
        health_data['database'] = f'error: {str(e)}'
        logger.error(f"Database health check failed: {str(e)}")
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        if result == 'ok':
            health_data['redis'] = 'connected'
        else:
            health_data['redis'] = 'error'
            health_data['status'] = 'unhealthy'
    except Exception as e:
        health_data['status'] = 'unhealthy'
        health_data['redis'] = f'error: {str(e)}'
        logger.error(f"Redis health check failed: {str(e)}")
    
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return JsonResponse(health_data, status=status_code)
