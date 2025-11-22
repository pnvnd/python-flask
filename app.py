import os
import requests

##########
# Traces #
##########
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

########
# Logs #
########
import logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

logger_provider = LoggerProvider()
set_logger_provider(logger_provider)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
logging.getLogger().addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))
logging.getLogger().setLevel(logging.INFO)

###########
# Metrics #
###########
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

metrics.set_meter_provider(MeterProvider(metric_readers=[PeriodicExportingMetricReader(OTLPMetricExporter())]))
hit_counter = metrics.get_meter(name="opentelemetry.instrumentation.custom", version="1.0.0").create_counter("hit.counter", unit="1", description="Measures the number of times an endpoint was hit.")

###################
# Instrumentation #
###################
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.jinja2 import Jinja2Instrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
# from opentelemetry.instrumentation.redis import RedisInstrumentor
# from opentelemetry.instrumentation.logging import LoggingInstrumentor

# Flask Web Application
from flask import Flask, render_template, jsonify
app = Flask(__name__, static_url_path='/', static_folder='application/static', template_folder='application/templates')

FlaskInstrumentor().instrument_app(app)
Jinja2Instrumentor().instrument()
# RequestsInstrumentor().instrument()
# URLLib3Instrumentor().instrument()
# RedisInstrumentor().instrument()
# LoggingInstrumentor().instrument()

# Navigation
@app.route("/")
def index():
    hit_counter.add(1, attributes={"route": "/"})
    return render_template("index.html", title="Flask Web Application")

@app.route("/ping", strict_slashes=False)
def ping():
    logging.info("Ping")
    hit_counter.add(1, attributes={"route": "/ping"})
    return jsonify(ping="pong")

@app.route("/about")
def about():
    hit_counter.add(1, attributes={"route": "/about"})
    return render_template("about.html", title="Datacrunch - About")

@app.route("/statuspage", strict_slashes=False)
def statuspage():
    logging.info("Statuspage")
    hit_counter.add(1, attributes={"route": "/statuspage"})
    return render_template("projects/statuspage.html", title="Simple Statuspage")

# API to convert Fahrenheit to Celcius, without error handling
@app.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    logging.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    hit_counter.add(1, attributes={"route": "/convertC"})
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit, with error handling
@app.route("/convertF/<tempC>")
def convertF(tempC):
    try:
        tempF = 9/5*(float(tempC))+32
        logging.info(f"[INFO] Converted {tempC}°F to {tempF:.2f}°C.")
        hit_counter.add(1, attributes={"route": "/convertF"})
        return f"{tempC}°C is {tempF:.2f}°F."
    except:
        logging.warning("[WARN] Invalid temperature!")
        hit_counter.add(1, attributes={"route": "/convertF"})

@app.route("/extfib/<int:n>")
def extfib(n):
    try:
        # Read endpoint from environment variable
        endpoint = os.environ.get("LAMBDA_ENDPOINT")
        if not endpoint:
            logging.error("[ERROR] LAMBDA_ENDPOINT environment variable not set.")
            return "Endpoint not configured", 500

        # Call external Lambda endpoint with ?n=<n>
        response = requests.get(f"{endpoint}", params={"n": n})
        response.raise_for_status()

        data = response.json()
        result = data.get("result")

        logging.info(f"[INFO] the {n}th Fibonacci number is {result}.")
        hit_counter.add(1, attributes={"route": "/extfib"})
        return str(result)

    except Exception as e:
        logging.warning(f"[WARN] Failed to fetch Fibonacci number: {e}")
        hit_counter.add(1, attributes={"route": "/extfib"})
        return "Error fetching result", 500

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
