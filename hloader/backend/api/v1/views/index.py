from flask import url_for
from werkzeug.utils import redirect

from hloader.backend.api import app

__author__ = 'dstein'

@app.route('/api/v1')
def api_v1():
    return "api_v1"
