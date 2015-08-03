import json
import pkgutil

from flask import request, Response

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'


@app.route('/api/v1/packages')
def packages():
    modules = []

    iter = pkgutil.iter_modules()
    while True:
        try:
            module = iter.next()
            modules.append(module[1])
        except:
            break

    return "modules: " + str(modules)