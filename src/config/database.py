from redis.asyncio import Redis
from .settings import settings

redis_client = Redis(host=settings.redis_config.HOST,
                     port=settings.redis_config.PORT,
                     db=0, password=settings.redis_config.PASS.get_secret_value(), decode_responses=True, )
