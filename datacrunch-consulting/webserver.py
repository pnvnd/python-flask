from flask import Flask, render_template, jsonify

# Flask Web Application
flaskapp = Flask(__name__, static_url_path="/")

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@flaskapp.route("/ping/", strict_slashes=False)
def ping():
    return jsonify(ping="pong")

@flaskapp.route("/about")
def about():
    return render_template("about.html", title="Datacrunch - About")

@flaskapp.route("/projects")
def projects():
    return render_template("projects.html", title="Datacrunch - Projects")

# API to convert Fahrenheit to Celcius
@flaskapp.route("/projects/convertC/<float:tempF>")
def convertC(tempF):
    return f"{tempF}°F is {(5/9*(float(tempF))-32):.2f}°C."

# API to convert Celcius to Fahrenheit
@flaskapp.route("/projects/convertF/<float:tempC>")
def convertF(tempC):
    return f"{tempC}°C is {9/5*(float(tempC))+32:.2f}°F."

### Add Applications Here ###

# API to calculate the nth prime number and how long it takes
from projects.prime import prime
flaskapp.register_blueprint(prime)

# API to calculate the nth fibonacci number
from projects.fibonacci import fibonacci
flaskapp.register_blueprint(fibonacci)

# Get COVID data and plot on chart
from projects.covid import covid
flaskapp.register_blueprint(covid)

# Run Flask Web Application
if __name__ == "__main__":
    flaskapp.run()
