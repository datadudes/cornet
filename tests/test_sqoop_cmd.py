
from cornet.sqoop_cmd import SqoopCmd
from cornet.connectors import Table, Column
from cornet.task_config import TaskConfig
import pytest


@pytest.mark.parametrize(("k", "v", "exp"), [
    ('delete-target-dir', True, '--delete-target-dir'),
    ('m', 10, '-m 10'),
    ('warehouse-dir', '/user/sqoop2', '--warehouse-dir /user/sqoop2'),
    ('f', True, '-f')])
def test_args2str(k, v, exp):
    assert SqoopCmd._arg2str(k, v) == exp


def test_arg_jdbc_url():
    task_config = {
        'source': {
            'driver': 'mysql',
            'host': 'example.com',
            'port': 12345,
            'db': 'portal',
            'user': 'datadudes',
            'password': 'hadoop-rocks'
        },
        'hive': {
            'db': 'raw_data',
            'table_prefix': 'p_'
        },
        'map_types': {
            'hive': {'VARBINARY': 'HiveType1', 'UUID': 'HiveType2'},
            'java': {'VARBINARY': 'JavaType1', 'VARCHAR': 'JavaType2'}
        },
        'sqoop_args': {
            'user': {
                'direct': True,
                'm': 5
            }
        }
    }
    task = TaskConfig(task_config, {})
    table = Table('user', 'TABLE')
    columns = [Column('id', 'VARCHAR'), Column('img', 'VARBINARY')]
    cmd = SqoopCmd(task, table, columns)
    assert cmd.args() == {
        'connect': 'jdbc:mysql://example.com:12345/portal',
        'hive-import': True,
        'hive-table': 'raw_data.p_user',
        'map-column-hive': 'img=HiveType1',
        'map-column-java': 'id=JavaType2,img=JavaType1',
        'password': '\'hadoop-rocks\'',
        'table': 'user',
        'username': 'datadudes',
        'direct': True,
        'm': 5
    }
