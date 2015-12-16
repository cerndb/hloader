import re
from flask import request



def get_username(username_from_request):
    """

    :param username_from_request:
    :return:
    """
    match = re.search("^(?:[^\\\\]*\\\\?)(.*)$", username_from_request)
    if match:
        return match.group(1)
    else:
        return request.remote_user
