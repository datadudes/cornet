from collections import namedtuple

Column = namedtuple('Column', ['name', 'type'])
Table = namedtuple('Table', ['name', 'type'])


def get_connector(source):
    driver = source['driver']
    if driver == 'mysql':
        from mysql_connector import MySqlConnector
        return MySqlConnector(source)
    elif driver == 'postgresql':
        from postgresql_connector import PostgreSqlConnector
        return PostgreSqlConnector(source)
    else:
        raise LookupError("Driver {0} not supported".format(driver))
