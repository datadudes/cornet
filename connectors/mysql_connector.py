import mysql.connector
from contextlib import closing


class MySQLConnector:

    def __init__(self, source):
        self.source = source

    def __enter__(self):
        self.connection = self._get_connection(self.source)
        return self

    def __exit__(self, type, value, traceback):
        self.connection.close()

    def get_tables(self):
        return self.query("show full tables")

    def get_table_schema(self, table_name):
        return self.query("describe `{0}`".format(table_name))

    def query(self, q):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(q)
            return cursor.fetchall()

    def _get_connection(self, source):
        connection = mysql.connector.connect(
            host=source['host'], port=source['port'],
            user=source['user'], passwd=source['password'],
            db=source['db'])
        return connection

    def jdbc_url_prefix(self):
        return 'jdbc:mysql'