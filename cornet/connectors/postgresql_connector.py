import psycopg2
from base_connector import BaseConnector
from cornet.connectors import Table, Column


class PostgreSqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:postgresql'

    def _get_db_conn(self):
        source = self.source
        return psycopg2.connect(
            host=source['host'],
            port=source['port'],
            user=source['user'],
            password=self._get_password(),
            database=source['db'])

    def get_tables(self):
        sql = """
            select table_name, table_type
            from information_schema.tables
            where table_schema NOT IN ('pg_catalog', 'information_schema'); """
        res = self.query(sql)
        return map(Table._make, res)

    def get_columns(self, table):
        sql = """
            select column_name, upper(udt_name)
            from information_schema.columns
            where table_catalog = '{0}'
            and table_name = '{1}'; """
        res = self.query(sql.format(self.source['db'], table.name))
        return map(Column._make, res)
