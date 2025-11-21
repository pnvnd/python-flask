from flask import Blueprint
import logging

logger = logging.getLogger(__name__)
luhn = Blueprint("luhn", __name__)

@luhn.route("/api/luhn/<cardNo>", strict_slashes=False)
def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
        if isSecond:
            d *= 2
        nSum += d // 10
        nSum += d % 10
        isSecond = not isSecond

    if nSum % 10 == 0:
        logger.info(f"Card number {cardNo} is valid.")
        return f"{cardNo} is a valid card number."
    else:
        logger.error(f"Card number {cardNo} is invalid.")
        return f"{cardNo} is NOT a valid card number."
