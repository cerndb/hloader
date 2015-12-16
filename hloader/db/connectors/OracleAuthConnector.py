from hloader.config import config

__author__ = 'dstein'
import cx_Oracle


class OracleAuthConnector(object):
    def __init__(self, address, port, username, password, SID):
        self._dsn = cx_Oracle.makedsn(address, port, SID)
        self._username = username
        self._password = password

        self.AUTH_TABLE = config.AUTH_TABLE
        self.AUTH_USERNAME_ATTR = config.AUTH_USERNAME_ATTR
        self.AUTH_DATABASE_ATTR = config.AUTH_DATABASE_ATTR
        self.AUTH_SCHEMA_ATTR = config.AUTH_SCHEMA_ATTR

    def _connect(self):
        connection = cx_Oracle.connect(user=self._username, password=self._password, dsn=self._dsn)
        return connection

    def get_servers_for_user(self, username):
        try:
            connection = self._connect()
            cursor = connection.cursor()

            query = "select {DATABASE_ATTR}, {SCHEMA_ATTR} from {TABLENAME} where upper({USERNAME_ATTR}) = :username".format(
                TABLENAME=self.AUTH_TABLE,
                USERNAME_ATTR=self.AUTH_USERNAME_ATTR,
                DATABASE_ATTR=self.AUTH_DATABASE_ATTR,
                SCHEMA_ATTR=self.AUTH_SCHEMA_ATTR
            )
            cursor.prepare(query)
            cursor.execute(None, {
                'username': username.upper()
            })

            raw = cursor.fetchall()

            databases = {}

            for (database, schema) in raw:
                if database not in databases:
                    databases.update({database: {"database": database, "schemas": []}})

                databases[database]["schemas"].append(schema)

            result = {"databases": databases.values()}

        except Exception as e:
            return str(e)

        finally:
            cursor.close()
            connection.close()

        return result

    def can_user_access_schema(self, username, database, schema):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            cursor.prepare(
                "select count(*) from {TABLENAME} where upper({USERNAME_ATTR}) = :username and upper({DATABASE_ATTR}) = :database and upper({SCHEMA_ATTR}) = :schema".format(
                    TABLENAME=self.AUTH_TABLE,
                    USERNAME_ATTR=self.AUTH_USERNAME_ATTR,
                    DATABASE_ATTR=self.AUTH_DATABASE_ATTR,
                    SCHEMA_ATTR=self.AUTH_SCHEMA_ATTR
                )
            )
            cursor.execute(None, {
                'username': username.upper(),
                'database': database.upper(),
                'schema': schema.upper()
            })
            result = cursor.fetchall()[0][0]

            try:
                return int(result) > 0
            except Exception:
                return False

        except Exception as e:
            # TODO raise
            # return str(e)
            return False
        finally:
            cursor.close()
            connection.close()

    def get_available_objects(self, database, schema):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            cursor.prepare(
                "select OBJECT_NAME, OBJECT_TYPE from table(cern_dba.get_user_objects(:database_name,:schema_name))"
            )
            cursor.execute(None, {
                'database_name': database.upper(),
                'schema_name': schema.upper()
            })

            raw = cursor.fetchall()

            result = map(lambda line: line[0], raw)
            return result

        except Exception as e:
            # TODO raise
            return str(e)
        finally:
            cursor.close()
            connection.close()