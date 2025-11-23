from flask import Blueprint, render_template
import logging

logger = logging.getLogger(__name__)
logger.propagate = True

# Flask Blueprint Application
covid = Blueprint("covid", __name__)

@covid.route("/covid", strict_slashes=False)
def main():
    import pandas as pd

    filename = "https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv"

    df = pd.read_csv(filename)
    logger.info(f"Download success: {filename}")
    covidtesting = df.to_json(orient="records")
   
    return render_template("projects/covid.html", covidtesting=covidtesting, msg="covidtesting.csv", title="Ontario COVID-19")
