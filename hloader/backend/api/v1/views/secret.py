from hloader.backend.api import app
from hloader.backend.api.v1.decorators.sso_secured import sso_secured

__author__ = 'dstein'

@app.route('/api/v1/secret')
@sso_secured
def secret():
    return 'secret boop'
