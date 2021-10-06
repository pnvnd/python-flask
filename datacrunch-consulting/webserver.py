from flask import Flask, render_template, request
from pywebio.platform.flask import webio_view

# Flask Web Application
flaskapp = Flask(__name__, static_url_path="/")

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@flaskapp.route("/about/")
def about():
    return render_template("about.html", title="Datacrunch - About")

@flaskapp.route("/projects/")
def projects():
    return render_template("projects.html", title="Datacrunch - Projects")

# Add Applications Here
from projects.covid import covid
flaskapp.register_blueprint(covid)

# from projects.snowflake import snowflakeApp
# flaskapp.register_blueprint(snowflakeApp)

# PyWebIO Integrated Application 1

# from projects.mongodb import *
# flaskapp.add_url_rule("/projects/pywebio/", "mongodbApp", webio_view(mongodbApp), methods=["GET", "POST"])

# PyWebIO Integrated Application 2
from projects.tempConvert import *
flaskapp.add_url_rule("/projects/tempconvert/", "tempConvert", webio_view(tempConvert), methods=["GET", "POST"])

# Run Flask Web Application
if __name__ == "__main__":
    flaskapp.run()