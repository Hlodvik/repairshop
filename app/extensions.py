from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow
from flask_caching import Cache

ma = Marshmallow()
limiter = Limiter(
    get_remote_address,
    default_limits=["60 per hour"],  
)  
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})