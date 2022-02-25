from flask import Blueprint, render_template, request

# Flask Blueprint Application
divisibility = Blueprint("divisibility", "divisibility")

@divisibility.route("/divisibility", strict_slashes=False)
def index():
    return render_template("projects/divisibility.html", title="Divisibility Checker")

@divisibility.route("/divisibility_result", strict_slashes=False, methods=['POST'])
def divisibility_result():

    # request.form looks for:
    # html tags with matching "name= "
    first_input = request.form['Input1']
    input1 = int(first_input)

    factors = []
    for n in range(2,input1):
        if input1%n ==0:
            factors.append(n)
        else:
            continue

    return render_template("projects/divisibility.html", title="Divisibility Results", input1=input1, factors=factors)
