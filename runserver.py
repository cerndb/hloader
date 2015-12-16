from hloader.api.v1 import app


class RunAPIServer(object):
    def __init__(self, **kwargs):
        app.run(**kwargs)