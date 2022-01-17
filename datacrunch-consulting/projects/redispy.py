from flask import Blueprint, render_template
import os
from urllib.parse import urlparse
import redis

# Flask Blueprint Application
redispy = Blueprint("redispy", "redispy")

url = urlparse(os.environ.get("REDIS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
# r = redis.Redis(host='localhost', port=6379, db=0)

@redispy.route("/projects/redis", strict_slashes=False)
def index():
    r.set('foo', 'bar')
    return r.get('foo')
