from cornet.task_config import TaskConfig
from cornet.connectors import Table


def test_yaml_load():
    tasks = [t for t in TaskConfig.load('tests/configs/sample.yaml')]
    assert len(tasks) == 2
    assert tasks[0].source == {
        'driver': 'mysql',
        'host': 'my.example.com',
        'port': 1111,
        'db': 'db1',
        'user': 'marcel',
        'password': 'datadude1'
    }
    assert tasks[0].hive == {
        'db': 'sqoop_test',
        'table_prefix': 'a_'
    }
    assert set(tasks[0].skip_tables) == {
        'schema_version',
        'log',
        'notification'
    }
    assert tasks[0].sqoop_args(Table('some_table', 'table')) == {
        'm': 2,
        'direct': True,
        'data-warehouse': '/user/sqoop'
    }
    assert tasks[0].sqoop_args(Table('user', 'table')) == {
        'm': 1,
        'direct': False,
        'data-warehouse': '/user/sqoop'
    }
