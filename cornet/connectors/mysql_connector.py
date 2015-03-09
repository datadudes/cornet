import MySQLdb
from base_connector import BaseConnector
from cornet.connectors import Table, Column


class MySqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:mysql'

    def _get_db_conn(self):
        source = self.source
        return MySQLdb.connect(
            host=source['host'],
            port=source['port'],
            user=source['user'],
            passwd=self._get_password(),
            db=source['db'])

    def get_tables(self):
        res = self.query("show full tables")
        return map(Table._make, res)

    def get_columns(self, table):
        sql = """
            select column_name, upper(data_type)
            from information_schema.columns
            where table_schema = '{0}'
            and table_name = '{1}' """
        res = self.query(sql.format(self.source['db'], table.name))
        return map(Column._make, res)
