from flask import Flask
from flask.ext.cors import CORS



app = Flask(__name__)

# CORS(app, resources=r"/api/*", allowed_headers="Content-Type")