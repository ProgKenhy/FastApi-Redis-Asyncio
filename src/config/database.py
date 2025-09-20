from redis import Redis
from .settings import settings

redis_client = Redis.from_url(
    str(settings.redis_config.REDIS_URL),
    decode_responses=True
)