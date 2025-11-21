##########################
# OpenTelemetry Settings #
##########################
from opentelemetry.sdk.resources import Resource
import uuid
serviceId = str(uuid.uuid1())

OTEL_RESOURCE_ATTRIBUTES = {
    "service.name": "python-flask.otel",
    "service.instance.id": serviceId,
    "environment": "vercel"
}

##########
# Traces #
##########
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider(resource=Resource.create(OTEL_RESOURCE_ATTRIBUTES)))
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

########
# Logs #
########
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

logger_provider = LoggerProvider(resource=Resource.create(OTEL_RESOURCE_ATTRIBUTES))
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))
logging.getLogger().setLevel(logging.INFO)

###################
# Instrumentation #
###################
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Flask Web Application
from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/', static_folder='application/static', template_folder='application/templates')

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
Jinja2Instrumentor().instrument()
URLLib3Instrumentor().instrument()
RedisInstrumentor().instrument()
LoggingInstrumentor().instrument()

# Navigation
@app.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@app.route("/ping", strict_slashes=False)
def ping():
    logging.info("Ping")
    return jsonify(ping="pong")

@app.route("/about")
def about():
    return render_template("about.html", title="Datacrunch - About")

@app.route("/statuspage", strict_slashes=False)
def statuspage():
    logging.info("Statuspage")
    return render_template("projects/statuspage.html", title="Simple Statuspage")

# API to convert Fahrenheit to Celcius
@app.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    logging.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit New Comment
@app.route("/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
        logging.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        return f"{tempC}°C is {tempF:.2f}°F."
    except:
        logging.warning("[WARN] Invalid temperature!")

### Add Applications Here #######

# API to calculate the nth prime number and how long it takes
from application.projects.prime import prime
app.register_blueprint(prime)

# API to calculate the nth fibonacci number
from application.projects.fibonacci import fibonacci
app.register_blueprint(fibonacci)

# API to validate credit card numbers
from application.projects.luhn import luhn
app.register_blueprint(luhn)

# Get COVID data and plot on chart
from application.projects.covid import covid
app.register_blueprint(covid)

# Test redis-py in App
from application.projects.redispy import redispy
app.register_blueprint(redispy)

# Input number to check divisibility
from application.projects.divisibility import divisibility
app.register_blueprint(divisibility)

# Run Flask Web Application, new comment
if __name__ == "__main__":
    app.run()
