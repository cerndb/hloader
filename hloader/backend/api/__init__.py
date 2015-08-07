from __future__ import absolute_import
from flask import Flask
from flask.ext.cors import CORS

__author__ = 'dstein'

app = Flask(__name__)

# CORS(app, resources=r"/api/*", allowed_headers="Content-Type")