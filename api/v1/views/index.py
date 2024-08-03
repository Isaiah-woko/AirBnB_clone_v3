#!/usr/bin/python3
"""a script for creating the /status route"""

from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status"""
    return jsonify({"status": "OK"})
