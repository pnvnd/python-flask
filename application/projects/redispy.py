from flask import Blueprint, render_template
import logging

logger = logging.getLogger(__name__)
logger.propagate = True

# Flask Blueprint Application
redispy = Blueprint("redispy", __name__)

@redispy.route("/redis", strict_slashes=False)
def index():
    import os
    import redis
    # from urllib.parse import urlparse
    
    ## Heroku
    r = redis.from_url(os.environ.get("REDIS_URL"))

    ## localhost
    # r = redis.Redis(host='localhost', port=6379, db=0)

    ## TLS Required
    # url = urlparse(os.environ.get("REDIS_URL"))
    # r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
    
    r.set('foo', 'bar')
    return r.get('foo')
