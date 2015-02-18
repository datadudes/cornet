import yaml
from jinja2 import Environment, FileSystemLoader
import copy


class TaskConfig():

    DEFAULT = {
        'source': {},
        'skip_tables': [],
        'hive': {
            'db': '',
            'table_prefix': ''
        }
    }

    def __init__(self, task_config, global_config):

        merged = TaskConfig._merge(TaskConfig._merge(
            TaskConfig._without_key(task_config, 'sqoop_args'),
            TaskConfig._without_key(global_config, 'sqoop_args')),
            TaskConfig.DEFAULT)

        for key in ['source', 'hive', 'skip_tables']:
            setattr(self, key, merged[key])

        self._config = task_config
        self._global_config = global_config

    def sqoop_args(self, table_name):
        return TaskConfig._merge(
            self._config.get('sqoop_args', {}).get(table_name, {}),
            self._global_config.get('sqoop_args', {}))

    # TODO: move to another class
    @staticmethod
    def _merge(a, b):
        """
        Merge dictionaries a and b recursively. If necessary, a overrides b .
        A new dictionary is returned, input arguments are not changed.
        """
        assert isinstance(a, dict), "First arg not a dict, but {0} ".format(a)
        assert isinstance(b, dict), "Second arg not a dict, but {0} ".format(b)

        merged = {}
        for key in set(a.keys() + b.keys()):
            if key not in b.keys():
                merged[key] = a[key]
            elif key not in a.keys():
                merged[key] = b[key]
            elif isinstance(a[key], dict) and isinstance(b[key], dict):
                merged[key] = TaskConfig._merge(a[key], b[key])
            else:
                merged[key] = a[key]
        return merged

    @staticmethod
    def load(filename):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(filename)
        yaml_str = template.render()
        conf = yaml.safe_load(yaml_str)
        global_conf = conf['global']
        for task_config in conf['tasks']:
            yield TaskConfig(task_config, global_conf)

    @staticmethod
    def _without_key(dict, key):
        """ Returned a new copy of dictionary without a specified key """
        d = copy.deepcopy(dict)
        if key in d:
            del d[key]
        return d
