#!/usr/bin/python3
"""a script for creating the /status route"""

from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status"""
    status = {
        "status": "OK"
    }
    response = jsonify(status)
    response.status_code = 200
    return response
