import psycopg2
from base_connector import BaseConnector


class PostgreSqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:postgres'

    def _get_db_conn(self):
        source = self.source
        return psycopg2.connect(
            host=source['host'], port=source['port'],
            user=source['user'], password=source['password'],
            database=source['db'])

    def get_tables(self):
        return self.query("""
            select table_name, table_type
            from information_schema.tables
            where table_schema NOT IN ('pg_catalog', 'information_schema');
        """)

    def get_columns(self, table):
        return self.query("describe `{0}`")

