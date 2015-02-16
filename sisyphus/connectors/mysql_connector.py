import MySQLdb
from base_connector import BaseConnector


class MySqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:mysql'

    def _get_db_conn(self):
        source = self.source
        return MySQLdb.connect(
            host=source['host'], port=source['port'],
            user=source['user'], passwd=source['password'],
            db=source['db'])

    def get_tables(self):
        return self.query("show full tables")

    def get_columns(self, table):
        sql = """
            select column_name, data_type
            from information_schema.columns
            where table_schema = '{0}'
            and table_name = '{1}' """
        return self.query(sql.format(self.source['db'], table))

