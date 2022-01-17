from flask import Blueprint, render_template
import os
import redis

# Flask Blueprint Application
redispy = Blueprint("redispy", "redispy")

@redispy.route("/projects/redis", strict_slashes=False)
def index():
    r = redis.from_url(os.environ.get("REDIS_URL"))
    r.set('foo', 'bar')
    return r.get('foo')
