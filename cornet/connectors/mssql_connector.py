import pymssql # yes I know, would be nice to use JDBC connector instead
import sys
from .base_connector import BaseConnector
from cornet.connectors import Table, Column


class MSSqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:sqlserver'

    if sys.version_info[0] < 3:
        raise("Sorry, MSSQL isn't yet happy on Python 2.")

    def _get_db_conn(self):
        source = self.source
        return pymssql.connect(
            host=source['host'],
            user=source['user'],
            password=self._get_password(),
            database=source['db'])

    def get_tables(self):
        sql = """
            select table_name, table_type
            from information_schema.tables
            where table_name NOT IN ('sysdiagrams'); """
        res = self.query(sql)
        return list(map(Table._make, res))

    def get_columns(self, table):
        sql = """
            select column_name, upper(data_type)
            from information_schema.columns
            where table_catalog = '{0}'
            and table_name = '{1}'; """
        res = self.query(sql.format(self.source['db'], table.name))
        return list(map(Column._make, res))
