

def get_connector(source):
    driver = source['driver']
    if driver == 'mysql':
        from MySqlConnector import MySqlConnector
        return MySqlConnector(source)
    elif driver == 'postgres':
        from PostgreSqlConnector import PostgreSqlConnector
        return PostgreSqlConnector(source)
    else:
        raise LookupError("Driver {0} not supported".format(driver))



