#!/usr/bin/python3
"""Creating a blueprint for the api"""

from flask import Blueprint

app_views = Blueprint('/api/v1', __name__, url_prefix='/api/v1')

# Wildcard import of everything
from api.v1.views.index import *
