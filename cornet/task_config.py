import yaml
from jinja2 import Environment, FileSystemLoader
from dict_utils import merge_dict, dict_without_key


class TaskConfig():

    DEFAULT = {
        'source': {},
        'skip_tables': [],
        'hive': {
            'db': '',
            'table_prefix': ''
        },
        'map_types': {}
    }

    def __init__(self, task_config, global_config):
        merged = merge_dict(merge_dict(
            dict_without_key(task_config, 'sqoop_args'),
            dict_without_key(global_config, 'sqoop_args')),
            TaskConfig.DEFAULT)
        for key in ['source', 'hive', 'skip_tables', 'map_types']:
            setattr(self, key, merged[key])
        self._config = task_config
        self._global_config = global_config

    def sqoop_args(self, table):
        return merge_dict(
            self._config.get('sqoop_args', {}).get(table.name, {}),
            self._global_config.get('sqoop_args', {}))


    @staticmethod
    def load(filename):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(filename)
        yaml_str = template.render()
        conf = yaml.safe_load(yaml_str)
        global_conf = conf['global']
        for task_config in conf['tasks']:
            yield TaskConfig(task_config, global_conf)

