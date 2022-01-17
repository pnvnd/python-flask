from flask import Blueprint, render_template
import os
import redis
# from urllib.parse import urlparse

# Flask Blueprint Application
redispy = Blueprint("redispy", "redispy")

@redispy.route("/projects/redis", strict_slashes=False)
def index():
    ## Heroku
    r = redis.from_url(os.environ.get("REDIS_URL"))

    ## localhost
    # r = redis.Redis(host='localhost', port=6379, db=0)

    ## TLS Required
    # url = urlparse(os.environ.get("REDIS_URL"))
    # r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
    
    r.set('foo', 'bar')
    return r.get('foo')
