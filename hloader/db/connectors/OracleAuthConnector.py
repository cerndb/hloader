from hloader.config import AUTH_TABLE, AUTH_USERNAME_ATTR, AUTH_SCHEMA_ATTR

__author__ = 'dstein'
import cx_Oracle


class OracleAuthConnector(object):
    def __init__(self, address, port, username, password, SID):
        self._dsn = cx_Oracle.makedsn(address, port, SID)
        self._username = username
        self._password = password

    def _connect(self):
        connection = cx_Oracle.connect(user=self._username, password=self._password, dsn=self._dsn)
        return connection

    def get_servers_for_user(self, username):
        try:
            connection = self._connect()
            cursor = connection.cursor()
            cursor.prepare("select * from {TABLENAME} where {USERNAME_ATTR} = :username".format(
                TABLENAME=AUTH_TABLE,
                USERNAME_ATTR=AUTH_USERNAME_ATTR
            ))
            cursor.execute(None, {'username': username})
            result = cursor.fetchall()
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
                "select count(*) from {TABLENAME} where {USERNAME_ATTR} = :username and {DATABASE_ATTR} = :database and {SCHEMA_ATTR} = :schema".format(
                    TABLENAME=AUTH_TABLE,
                    USERNAME_ATTR=AUTH_USERNAME_ATTR,
                    SCHEMA_ATTR=AUTH_SCHEMA_ATTR
                )
            )
            cursor.execute(None, {'login': username, 'database': database, 'schema': schema})
            result = cursor.fetchall()[0][0]
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
            connection.close()

        return result
