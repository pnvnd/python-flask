import newrelic.agent
newrelic.agent.initialize()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Import the logging module and the New Relic log formatter
import logging
from newrelic.agent import NewRelicContextFormatter

# Instantiate a new log handler, and set logging level
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Instantiate the log formatter and add it to the log handler
formatter = NewRelicContextFormatter()
handler.setFormatter(formatter)

# Get the root logger, set logging level, and add the handler to it
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

# Flask Web Application
from flask import Flask, render_template, jsonify
flaskapp = Flask(__name__, static_url_path='/', static_folder='application/static', template_folder='application/templates')

# OpenTelemetry Settings
import uuid
trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "python-flask.otel", "service.instance.id": str(uuid.uuid1()), "environment": "development"})))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

FlaskInstrumentor().instrument_app(flaskapp)
RequestsInstrumentor().instrument()
Jinja2Instrumentor().instrument()
URLLib3Instrumentor().instrument()
RedisInstrumentor().instrument()
LoggingInstrumentor().instrument()

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@flaskapp.route("/ping", strict_slashes=False)
def ping():
    return jsonify(ping="pong")

@flaskapp.route("/about")
def about():
    return render_template("about.html", title="Datacrunch - About")

@flaskapp.route("/statuspage", strict_slashes=False)
def statuspage():
    return render_template("projects/statuspage.html", title="Simple Statuspage")

# API to convert Fahrenheit to Celcius
@flaskapp.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    root_logger.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit
@flaskapp.route("/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
        root_logger.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        return f"{tempC}°C is {tempF:.2f}°F."
    except:
        root_logger.warning("[WARN] Invalid temperature!")

### Add Applications Here ###

# API to calculate the nth prime number and how long it takes
from application.projects.prime import prime
flaskapp.register_blueprint(prime)

# API to calculate the nth fibonacci number
from application.projects.fibonacci import fibonacci
flaskapp.register_blueprint(fibonacci)

# API to validate credit card numbers
from application.projects.luhn import luhn
flaskapp.register_blueprint(luhn)

# Get COVID data and plot on chart
from application.projects.covid import covid
flaskapp.register_blueprint(covid)

# Test redis-py in App
from application.projects.redispy import redispy
flaskapp.register_blueprint(redispy)

# Input number to check divisibility
from application.projects.divisibility import divisibility
flaskapp.register_blueprint(divisibility)

# Run Flask Web Application, new comment
if __name__ == "__main__":
    flaskapp.run()