
import click
from connectors import get_connector
from config import TaskConfig


def get_sqoop_args(task, table, jdbc_url_prefix, columns):
    basic_args = {
        'connect': jdbc_url(task, jdbc_url_prefix),
        'username': task.source['user'],
        'password': task.source['password'],
        'table': table,
        'hive-import': True,
        'hive-overwrite': True,
        'map-column-hive': get_type_mappings(task, columns),
        'direct': True,
        'hive-table': hive_table(task, table)
    }
    custom_args = task.sqoop_args(table)
    return TaskConfig._merge(custom_args, basic_args)


def jdbc_url(task, jdbc_url_prefix):
    return '{0}://{1}:{2}/{3}'.format(
        jdbc_url_prefix, task.source['host'],
        task.source['port'], task.source['db'])


def hive_table(task, table):
    return '{0}.{1}{2}'.format(task.hive['db'], task.hive['table_prefix'], table)


def sqoop_arg_to_str(k, v):
    prefix = '-' if len(k) == 1 else '--'
    value = '' if isinstance(v, bool) else v
    return '{0}{1} {2}'.format(prefix, k, value).strip()

def sqoop_args_to_cmd(args):
    cmd_args = {sqoop_arg_to_str(k, v) for k, v in args.iteritems() if v}
    return ' \\\n   '.join(['sqoop import'] + sorted(cmd_args)) + '\n'


def get_type_mappings(task, columns):
    type_mapping = task.hive.get('map-types', {})
    mapped_columns = [
        "{0}={1}".format(c_name, type_mapping[c_type.upper()])
        for c_name, c_type in columns
        if c_type.upper() in type_mapping]
    return ','.join(mapped_columns) if mapped_columns else False


def print_sqoop_cmds(task):
    with get_connector(task.source) as conn:
        tables_all = conn.get_tables()
        to_skip = task.source.get('skip_tables', [])
        to_import = [t[0] for t in tables_all if t[0] not in to_skip]
        for table in sorted(to_import):
            columns = conn.get_columns(table)
            args = get_sqoop_args(task, table, conn.jdbc_url_prefix, columns)
            print sqoop_args_to_cmd(args)


def print_schema(task):
    with get_connector(task.source) as conn:
        tables_all = conn.get_tables()
        for table in tables_all:
            print '\n=== {0}.{1} ==='.format(task.source['db'], table[0])
            columns = conn.get_columns(table[0])
            for c in columns:
                print '{0}: {1}'.format(c[0], c[1].upper())


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--print-schema-only', is_flag=True)
def cli(config_file, print_schema_only):
    for task in TaskConfig.load(config_file):
        if print_schema_only:
            print_schema(task)
        else:
            print_sqoop_cmds(task)
