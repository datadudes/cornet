
import yaml
from jinja2 import Environment, FileSystemLoader
import click
from connectors import get_connector


def get_conf(filename):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(filename)
    yaml_str = template.render()
    return yaml.safe_load(yaml_str)


def get_sqoop_cmd(task_config, table, jdbc_url_prefix):
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


def print_sqoop_cmds(task_config):
    source = task_config['source']
    with get_connector(source) as conn:
        tables_all = conn.get_tables()
        to_skip = source.get('skip_tables', [])
        to_import = [t for t in tables_all if t[0] not in to_skip]
        for table in sorted(to_import):
            cmd = get_sqoop_cmd(task_config, table, conn.jdbc_url_prefix)
            print cmd


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
def cli(config_file):
    conf = get_conf(config_file)
    for task_name, task_config in conf.iteritems():
        print_sqoop_cmds(task_config)
