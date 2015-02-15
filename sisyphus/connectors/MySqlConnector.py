import mysql.connector
from BaseConnector import BaseConnector


class MySqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:mysql'

    def _get_db_conn(self):
        source = self.source
        return mysql.connector.connect(
            host=source['host'], port=source['port'],
            user=source['user'], passwd=source['password'],
            db=source['db'])

    def get_tables(self):
        return self.query("show full tables")

    def get_columns(self, table):
        return self.query("describe `{0}`")

