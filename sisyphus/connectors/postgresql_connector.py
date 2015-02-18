import psycopg2
from base_connector import BaseConnector


class PostgreSqlConnector(BaseConnector):

    jdbc_url_prefix = 'jdbc:postgresql'

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
        sql = """
            select column_name, udt_name
            from information_schema.columns
            where table_name = '{0}'
            and table_catalog = '{1}'; """
        return self.query(sql.format(table, self.source['db']))
