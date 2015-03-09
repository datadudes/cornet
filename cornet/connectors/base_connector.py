from contextlib import closing


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

    def _get_password(self):
        if 'password' in self.source:
            return self.source['password']
        else:
            with open(self.source['password_file'], 'r') as f:
                return f.readline().strip()
