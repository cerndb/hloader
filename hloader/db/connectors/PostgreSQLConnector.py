import psycopg2
import psycopg2.extras
import sys


class PostgreSQLConnector(object):
    def __init__(self, host, dbname, port, user, password):
        try:
            self.connection = psycopg2.connect(
                host=host,
                database=dbname,
                port=port,
                user=user,
                password=password
            )
            self.connection.autocommit = True
        except:
            print "Unable to connect to the Postgres server"
            sys.exit()

        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )

        self.cursor.execute('SHOW server_version')
        version = self.cursor.fetchone()['server_version']
        print "Successfully connected to the PostgreSQL Server (%s)" % (version)
        print "Host:", host
        print "Database:", dbname
        print "User:", user

    def get_servers(self, **kwargs):
        """
        Queries the HL_SERVERS table and returns a list of Oracle servers based on the keyword arguments passed
        :param kwargs: Zero or more of the following arguments - server_id, server_port, server_name, server_address
        :return:

        :
        """
        real_kwargs = [(key, value) for key, value in kwargs.items() if value is not None]
        if bool(real_kwargs):
            where = ""
            i = 0
            for key, value in real_kwargs:
                where += "%s='%s'" % (key, value)
                i += 1
                if i != len(real_kwargs):
                    where += " AND "

            self.cursor.execute("SELECT * FROM HL_SERVERS WHERE %s" % (where,))
        else:
            self.cursor.execute("SELECT * FROM HL_SERVERS")

        servers = self.cursor.fetchall()
        return servers

    def get_jobs(self, job_id=None):
        if job_id is None:
            self.cursor.execute('SELECT * FROM HL_JOBS')
            servers = self.cursor.fetchone()
        else:
            self.cursor.execute("SELECT * FROM HL_JOBS WHERE job_id='{id}'", (job_id, ))
            servers = self.cursor.fetchall()
        return servers

    def add_server(self, oracle_server):
        """
        Add a new instance of @OracleServer into HL_SERVERS
        :return: server_id of the new instance of @OracleServer
        """
        try:
            self.cursor.execute(
                """INSERT INTO HL_SERVERS
                    (server_address, server_port, server_name)
                VALUES
                    (%s, %s, %s)
                RETURNING server_id""", (oracle_server.server_address,
                                         oracle_server.server_port, oracle_server.server_name)
            )

        except:
            print "Unable to add new server to Postgres table HL_SERVERS"
            sys.exit()

        return self.cursor.fetchone()['server_id']

    def get_clusters(self):
        pass

    def get_ready_jobs(self):
        pass

    def get_transfers(self, job="*", state="*", limit="10"):
        pass
