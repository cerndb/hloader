import os
from flask import request

from hloader.backend.api import app

@app.route("/headers")
def headers():
    httpBreak = "<br>"
    output = "<b>PYTHON ENVIRONMENT VARIABLES</b>" + httpBreak
    for key in os.environ.keys():
        output += "{0} = {1}{linebreak}".format(key, os.environ[key], linebreak=httpBreak)
    output += httpBreak + httpBreak + "<b>REQUEST HEADERS</b>" + httpBreak
    for key in request.headers.keys():
        output += "{0} = {1}{linebreak}".format(key, request.headers[key], linebreak=httpBreak)
    if request.remote_user is not None:
        output += httpBreak + httpBreak + "<b>request.remote_user</b>" + httpBreak
        output += request.remote_user + httpBreak

    return output
