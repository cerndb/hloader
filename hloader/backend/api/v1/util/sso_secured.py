from functools import wraps
from flask import redirect, request

__SSO_NEEDED = True


def sso_secured(function):
    """

    :param function:
    :return:
    """

    @wraps(function)
    def secured_function(*args, **kwargs):
        print('checking SSO')
        if __SSO_NEEDED and not request.remote_user:
            return redirect("https://login.cern.ch/adfs/ls/?wa=wsignin1.0&wtrealm=" + request.headers.url)
        else:
            return function(*args, **kwargs)

    return secured_function
