
import yaml
from jinja2 import Environment, FileSystemLoader
import click
from connectors import get_connector


def get_conf(filename):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(filename)
    yaml_str = template.render()
    return yaml.safe_load(yaml_str)


def get_sqoop_cmd(task_config, table_name, jdbc_url_prefix, columns):
    source = task_config['source']
    hive = task_config['hive']

    jdbc_url = '{0}://{1}:{2}/{3}'.format(jdbc_url_prefix,
        source['host'], source['port'], source['db'])

    map_column_hive = get_type_mappings(hive.get('type_mapping', {}), columns)
    hive_table = '{0}{1}'.format(hive['prefix'], table_name)

    template = """sqoop import
        --connect {0} --username {1} --password '{2}'
        --table {3}
        --hive-import --hive-overwrite --direct
        --hive-table {4}
        {5}
        """.replace('\n', ' \\\n')

    return template.format(
        jdbc_url,
        source['user'],
        source['password'],
        table_name,
        hive_table,
        map_column_hive)


def get_type_mappings(type_mappings, columns):
    mapped_columns = [
        "{0}={1}".format(c_name, type_mappings[c_type.upper()])
        for c_name, c_type in columns
        if c_type.upper() in type_mappings]

    if mapped_columns:
        return '--map-column-hive ' + ','.join(mapped_columns)
    else:
        return ''


def print_sqoop_cmds(task_config):
    source = task_config['source']
    with get_connector(source) as conn:
        tables_all = conn.get_tables()
        to_skip = source.get('skip_tables', [])
        to_import = [t[0] for t in tables_all if t[0] not in to_skip]
        for table_name in sorted(to_import):
            columns = conn.get_columns(table_name)
            cmd = get_sqoop_cmd(task_config, table_name,
                conn.jdbc_url_prefix, columns)
            print cmd


def print_schema(task_name, source):
    with get_connector(source) as conn:
        tables_all = conn.get_tables()
        for table in tables_all:
            print '\n=== {0}.{1} ==='.format(task_name, table[0])
            columns = conn.get_columns(table[0])
            for c in columns:
                print '{0}: {1}'.format(c[0], c[1].upper())


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--print-schema-only', is_flag=True)
def cli(config_file, print_schema_only):
    conf = get_conf(config_file)
    for task_name, task_config in conf.iteritems():
        if print_schema_only:
            print_schema(task_name, task_config['source'])
        else:
            print_sqoop_cmds(task_config)
