from __future__ import absolute_import
from flask import Flask
from flask_cors import CORS

__author__ = 'dstein'

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": "*"
    }
})