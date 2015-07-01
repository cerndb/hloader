import psycopg2
import sys

class PostgreSQLConnector:
    def __init__(self, host, dbname, user, password):
        try:
            self.connection = psycopg2.connect("host='%s' dbname='%s' user='%s' password='%s'"%(host, dbname, user, password))
        except:
            print "Unable to connect to the Postgres server"
            sys.exit()
        self.cursor = self.connection.cursor()
        self.cursor.execute('SHOW server_version')
        version = self.cursor.fetchone()[0]
        print "Successfully connected to the PostgreSQL Server (%s)"%(version)
        print "Host: ", host
        print "Database: ", dbname
        print "User: ", user


    def get_servers(self):
        pass

    def get_clusters(self):
        pass

    def get_jobs(self, database="*"):
        pass

    def get_ready_jobs(self):
        pass

    def get_transfers(self, job="*", state="*", limit="10"):
        pass
