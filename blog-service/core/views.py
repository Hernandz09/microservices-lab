from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def healthcheck(request):
    """
    Endpoint de healthcheck que verifica:
    - Conexión a PostgreSQL
    - Conexión a Redis
    """
    health_status = {
        'status': 'healthy',
        'checks': {
            'database': 'unknown',
            'redis': 'unknown'
        }
    }
    
    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = f'error: {str(e)}'
        logger.error(f"Database health check failed: {str(e)}")
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        if result == 'ok':
            health_status['checks']['redis'] = 'ok'
        else:
            health_status['checks']['redis'] = 'error: unexpected value'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['redis'] = f'error: {str(e)}'
        logger.error(f"Redis health check failed: {str(e)}")
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)
