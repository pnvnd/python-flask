from flask import Blueprint
import logging

logger = logging.getLogger(__name__)
logger.propagate = True

# Flask Blueprint Application
prime = Blueprint("prime", __name__)

@prime.route("/api/prime/<int:n>", strict_slashes=False)

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

    logger.info(f"{a-1} is prime number #{n}. Calculated in {end-start} seconds.")

    return f"{a-1} is prime number #{n}. Calculated in {end-start} seconds."
