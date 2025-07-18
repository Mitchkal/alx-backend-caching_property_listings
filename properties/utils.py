from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')

    if not properties:
        properties = list(Property.objects.all().values())
        cache.set('all_properties', properties, timeout=3600)
    return properties

def get_redis_cache_metrics():
    """
    Returns metrics on hits/misses for redis cache
    """
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total_requests = hits + misses

    hit_ratio = (hits / total_requests) if total_requests > 0 else 0

    metrics = {
        'hits': hits,
        'misses': misses,
        'hit_ratio': round(hit_ratio, 4)
    }
    try:
        logger.info(f"[Redis Cache Metrics] {metrics}")
    except Exception as e:
        logger.error(f"Error logging Redis cache metrics: {e}")
    return metrics