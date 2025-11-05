"""
Health check para el servicio de email.
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger('utils')


def healthcheck(request):
    """
    Endpoint de health check que verifica:
    - Conexión a la base de datos
    - Conexión a Redis
    """
    checks = {}
    overall_status = 'healthy'
    status_code = 200
    
    # Verificar base de datos
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
        overall_status = 'unhealthy'
        status_code = 503
        logger.error(f"Database health check failed: {str(e)}")
    
    # Verificar Redis
    try:
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        if result == 'ok':
            checks['redis'] = 'ok'
        else:
            raise Exception('Redis returned unexpected value')
    except Exception as e:
        checks['redis'] = f'error: {str(e)}'
        overall_status = 'unhealthy'
        status_code = 503
        logger.error(f"Redis health check failed: {str(e)}")
    
    return JsonResponse(
        {
            'status': overall_status,
            'checks': checks
        },
        status=status_code
    )
