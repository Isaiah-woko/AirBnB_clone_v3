#!/usr/bin/python3
"""The app for the api"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(exception):
    """handles the 404 error"""
    status = {
        "error": "Not found"
    }
    response = jsonify(status)
    response.status_code = 404

    return (response)


if __name__ == "__main__":

    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True)
