import re
from flask import request

__author__ = 'dstein'

def get_username(username_from_request):
    match = re.search("^(?:[^\\\\]*\\\\?)(.*)$", username_from_request)
    if match:
        return match.group(1)
    else:
        return request.remote_user