import psycopg2
from base_connector import BaseConnector, Column, Table


class PostgreSqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:postgresql'

    def _get_db_conn(self):
        source = self.source
        return psycopg2.connect(
            host=source['host'], port=source['port'],
            user=source['user'], password=source['password'],
            database=source['db'])

    def get_tables(self):
        return map(Table._make, self.query("""
            select table_name, table_type
            from information_schema.tables
            where table_schema NOT IN ('pg_catalog', 'information_schema');
        """))

    def get_columns(self, table):
        sql = """
            select column_name, upper(udt_name)
            from information_schema.columns
            where table_name = '{0}'
            and table_catalog = '{1}'; """
        return map(Column._make, self.query(sql.format(self.source['db'], table)))
