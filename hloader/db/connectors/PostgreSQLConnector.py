import psycopg2
import psycopg2.extras
import sys

class PostgreSQLConnector:
    def __init__(self, host, dbname, port, user, password):
        try:
            self.connection = psycopg2.connect(
                "host='%s' dbname='%s' port='%s' user='%s' \
                password='%s'"%(host, dbname, port, user, password))
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
        print "Successfully connected to the PostgreSQL Server (%s)"%(version)
        print "Host:", host
        print "Database:", dbname
        print "User:", user


    def get_servers(self):
        self.cursor.execute('SELECT * FROM HL_SERVERS')
        servers = self.cursor.fetchall()
        return servers

    def add_server(self, address, port, name):
        try:
            self.cursor.execute(
            """INSERT INTO HL_SERVERS
                    (server_address, server_port, server_name)
                VALUES
                    (%s, %s, %s)
                RETURNING server_id""", (address, port, name))

        except:
            print("Unable to add new server to Postgres table HL_SERVERS")
            sys.exit()

        return self.cursor.fetchone()['server_id']

    def get_clusters(self):
        pass

    def get_jobs(self, database="*"):
        pass

    def get_ready_jobs(self):
        pass

    def get_transfers(self, job="*", state="*", limit="10"):
        pass
