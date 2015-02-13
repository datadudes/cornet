
import yaml
from jinja2 import Environment, FileSystemLoader
from connectors import MySQLConnector

def get_conf(filename):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(filename)
    yaml_str = template.render()
    return yaml.safe_load(yaml_str)


def get_sqoop_cmd(task_config, table, schema, jdbc_url_prefix):
    source = task_config['source']
    hive = task_config['hive']
    table_name = table[0]

    jdbc_url  = '{0}://{1}:{2}/{3}'.format(jdbc_url_prefix,
        source['host'], source['port'], source['db'])

    hive_table = '{0}{1}'.format(hive['prefix'], table_name)

    return """sqoop import
            --connect {0} --username {1} --password '{2}'
            --table {3}
            --hive-import --hive-overwrite --direct
            --hive-table {4}
        """.replace('\n', ' \\\n').format(jdbc_url,
            source['user'], source['password'], table_name,
            hive_table)


conf = get_conf('ingest-conf.jinja')
print(conf)

for task_name, task_config in conf.iteritems():
    source = task_config['source']
    with MySQLConnector(source) as conn:
        tables_all = conn.get_tables()
        to_skip = source.get('skip_tables', [])
        to_import = [t for t in tables_all if t[0] not in to_skip]
        for table in sorted(to_import):
            schema = conn.get_table_schema(table[0])
            prefix = conn.jdbc_url_prefix()
            print get_sqoop_cmd(task_config, table, schema, prefix)


