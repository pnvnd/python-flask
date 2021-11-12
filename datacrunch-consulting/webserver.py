from flask import Flask, render_template, request

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

# Run Flask Web Application
if __name__ == "__main__":
    flaskapp.run()