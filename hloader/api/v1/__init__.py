from __future__ import absolute_import

from flask import Flask
app = Flask(__name__)

from hloader.api.v1 import views