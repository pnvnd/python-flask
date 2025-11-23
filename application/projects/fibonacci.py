from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)
logger.propagate = True

# Flask Blueprint Application
fibonacci = Blueprint("fib", __name__)

@fibonacci.route("/api/fib/<int:x>", strict_slashes=False)

def fib(x):
    array = [0, 1]

    for n in range(2, x + 1):
        array.append(array[n - 1] + array[n - 2])

    logger.info(f"Fibonacci number {x} is {array[x]}.")

    return jsonify(
        fibonacci_index=x,
        fibonacci_number=array[x]
    )

    #return f"{{\"fibonacci\": {{\"index_{x}\":\"{array[x]}\"}}}}"
