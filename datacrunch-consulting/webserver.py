from flask import Flask, render_template, request

# Flask Web Application
flaskapp = Flask(__name__, static_url_path="/")

# Navigation
@flaskapp.route("/")
def index():
    return render_template("index.html", title="Flask Web Application")

@flaskapp.route("/ping/")
def ping():
    return render_template("ping.html", title="Flask Web Application")

@flaskapp.route("/about/")
def about():
    return render_template("about.html", title="Datacrunch - About")

@flaskapp.route("/projects/")
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

# API to calculate the nth prime number and how long it takes
@flaskapp.route("/projects/prime/<int:n>")
def getPrime(n):
    import time
    
    start = time.time()
    count = 0
    a = 2

    while (count < n):
        b = 2
        prime = 1 # Check if prime number is found
        
        while (b * b <= a):
            if (a % b == 0):
                prime = 0
                break
            b += 1
            
        if (prime > 0):
            count += 1
            
        a += 1

    end = time.time()

    return f"{a-1} is prime number #{n}. Calculated in {end-start} seconds."

# Add Applications Here
from projects.covid import covid
flaskapp.register_blueprint(covid)

# Run Flask Web Application
if __name__ == "__main__":
    flaskapp.run()