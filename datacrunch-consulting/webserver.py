import newrelic.agent
newrelic.agent.initialize()

import logging
from flask import Flask, render_template, jsonify

# Set up logging
logger = logging.getLogger("Basic Logger")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Flask Web Application
flaskapp = Flask(__name__, static_url_path="/")

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Demo Application")

@flaskapp.route("/ping/", strict_slashes=False)
def ping():
    return jsonify(ping="pong")

# API to convert Fahrenheit to Celcius
@flaskapp.route("/convertC/<tempF>")
def convertC(tempF):
    tempC = (5/9*(float(tempF))-32)
    logger.info(f"[INFO] Converted {tempF}°F to {tempC:.2f}°C.")
    return f"{tempF}°F is {tempC:.2f}°C."

# API to convert Celcius to Fahrenheit
@flaskapp.route("/convertF/<tempC>")
def convertF(tempC):
    tempF = 9/5*(float(tempC))+32
    logger.info(f"[INFO] Converted {tempC}°C to {tempF:.2f}°F")
    return f"{tempC}°C is {tempF:.2f}°F."

# Run Flask Web Application
if __name__ == "__main__":
    flaskapp.run()
