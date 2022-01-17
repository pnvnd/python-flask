from flask import Blueprint, render_template
import redis

# Flask Blueprint Application
redispy = Blueprint("redispy", "redispy")

@redispy.route("/projects/redis", strict_slashes=False)
def index():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    return r.get('foo')
