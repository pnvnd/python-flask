from flask import Blueprint
import logging

# Instantiate a new log handler, and set logging level
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Instantiate the log formatter and add it to the log handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Get the root logger, set logging level, and add the handler to it
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(handler)

# Flask Blueprint Application
luhn = Blueprint("luhn", "luhn")

@luhn.route("/api/luhn/<cardNo>", strict_slashes=False)

def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle cases that make two digits after doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        root_logger.info(f"[INFO] Card number {cardNo} is valid.")
        return f"{cardNo} is a valid card number."
    else:
        root_logger.error(f"[ERROR] Card number {cardNo} is invalid.")
        return f"{cardNo} is NOT a valid card number."
