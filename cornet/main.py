import click
from connectors import get_connector
from task_config import TaskConfig
from sqoop_cmd import SqoopCmd
from utils import match_any


def print_sqoop_cmds(task):
    with get_connector(task.source) as conn:
        to_import = get_tables_to_import(conn, task)
        for table in sorted(to_import, key=lambda tbl: tbl.name):
            columns = conn.get_columns(table)
            cmd = SqoopCmd(task, table, columns)
            print cmd.as_string()


def get_tables_to_import(conn, task):
    all_tables = conn.get_tables()
    is_imported = lambda table: not task.import_tables or \
        match_any(task.import_tables, table.name)
    is_skipped = lambda table: match_any(task.skip_tables, table.name)
    return [t for t in all_tables if is_imported(t) and not is_skipped(t)]


def print_schema(task):
    with get_connector(task.source) as conn:
        to_import = get_tables_to_import(conn, task)
        for table in to_import:
            print '\n=== {0}.{1} ==='.format(task.source['db'], table[0])
            columns = conn.get_columns(table)
            for c in columns:
                print '{0}: {1}'.format(c.name, c.type)


@click.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--print-schema-only', is_flag=True)
def cli(config_file, print_schema_only):
    for task in TaskConfig.load(config_file):
        if print_schema_only:
            print_schema(task)
        else:
            print_sqoop_cmds(task)
