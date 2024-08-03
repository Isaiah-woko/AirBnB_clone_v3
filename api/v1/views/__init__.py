#!/usr/bin/python3
"""Creating a blueprint for the api"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything from the package api.v1.views.index
from .index import *
