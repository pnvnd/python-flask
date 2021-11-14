from flask import Blueprint, jsonify

# Flask Blueprint Application
fibonacci = Blueprint("fib", "fib")

@fibonacci.route("/projects/fib/<int:x>", strict_slashes=False)

def fib(x):
    array = [0, 1]

    for n in range(2, x + 1):
        array.append(array[n - 1] + array[n - 2])
    return jsonify(
        fibonacci_index=x,
        fibonacci_number=array[x]
    )

    #return f"{{\"fibonacci\": {{\"index_{x}\":\"{array[x]}\"}}}}"
