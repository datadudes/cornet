
import click
from connectors import get_connector
from task_config import TaskConfig
from sqoop_cmd import SqoopCmd


def print_sqoop_cmds(task):
    with get_connector(task.source) as conn:
        all_tables = conn.get_tables()
        to_import = [t for t in all_tables if t.name not in task.skip_tables]
        for table in sorted(to_import, key=lambda tbl: tbl.name):
            columns = conn.get_columns(table)
            cmd = SqoopCmd(task, table, columns)
            print cmd.as_string()


def print_schema(task):
    with get_connector(task.source) as conn:
        tables_all = conn.get_tables()
        for table in tables_all:
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
