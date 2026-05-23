import os
import logging
from datetime import datetime
from flask import Blueprint, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = "sample_weatherdata"
COLLECTION_NAME = "data"

logger = logging.getLogger(__name__)
logger.propagate = True

# Flask Blueprint Application
mongodb = Blueprint("mongodb", __name__)

def _format_doc(doc):
    return {
        "st": doc.get("st"),
        "ts": doc.get("ts").isoformat() if isinstance(doc.get("ts"), datetime) else str(doc.get("ts")),
        "elevation": doc.get("elevation"),
        "callLetters": doc.get("callLetters"),
        "airTemperature": doc.get("airTemperature", {}).get("value"),
        "dewPoint": doc.get("dewPoint", {}).get("value"),
        "pressure": doc.get("pressure", {}).get("value"),
        "windSpeed": doc.get("wind", {}).get("speed", {}).get("rate"),
        "visibility": doc.get("visibility", {}).get("distance", {}).get("value"),
    }

@mongodb.route("/mongodb", strict_slashes=False)
def index():
    try:
        client = MongoClient(MONGODB_URI, server_api=ServerApi("1"))
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        # get total count of documents in the collection
        total_count = collection.count_documents({})
        docs = list(collection.find().limit(10))
        rows = [_format_doc(doc) for doc in docs]
        return render_template(
            "projects/mongodb.html",
            title="MongoDB Atlas Weather Data",
            rows=rows,
            total_count=total_count,
        )
    except Exception as e:
        logger.exception("Failed to load MongoDB documents")
        return render_template(
            "projects/mongodb.html",
            title="MongoDB Atlas Weather Data",
            rows=[],
            error=str(e),
        ), 500
