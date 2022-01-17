from flask import Blueprint
import logging

logger = logging.getLogger("Basic Logger")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# Flask Blueprint Application
luhn = Blueprint("luhn", "luhn")

@luhn.route("/projects/luhn/<cardNo>", strict_slashes=False)

def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        logger.info(f"[INFO] Card number {cardNo} is valid.")
        return f"{cardNo} is a valid card number."
    else:
        logger.info(f"[INFO] Card number {cardNo} is invalid.")
        return f"{cardNo} is NOT a valid card number."
