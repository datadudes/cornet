from contextlib import closing
from collections import namedtuple

Column = namedtuple('Column', ['name', 'type'])
Table = namedtuple('Table', ['name', 'type'])


class BaseConnector:

    def __init__(self, source):
        self.source = source

    def __enter__(self):
        self.db_conn = self._get_db_conn()
        return self

    def __exit__(self, type, value, traceback):
        self.db_conn.close()

    def _get_db_conn(self):
        raise NotImplementedError()

    def query(self, q):
        with closing(self.db_conn.cursor()) as cursor:
            cursor.execute(q)
            return cursor.fetchall()
