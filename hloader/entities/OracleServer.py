class OracleServer(object):
    server_id = None
    server_address = None
    server_port = None
    server_name = None

    def __init__(self, server_address, server_port, server_name):
        self.server_address = server_address
        self.server_port = server_port
        self.server_name = server_name
