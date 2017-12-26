from utils import merge_dict


class SqoopCmd:

    def __init__(self, task, table, columns):
        self.task = task
        self.table = table
        self.columns = columns

    def _arg_jdbc_url(self):
        return 'jdbc:{0}://{1}:{2}/{3}'.format(
            self.task.source['driver'],
            self.task.source['host'],
            self.task.source['port'],
            self.task.source['db'])

    def _arg_jvmargs(self):
        return ["-D{0}={1}".format(k, v)
                for k, v in self.task.jvmargs.iteritems()]

    def _arg_hive_tablename(self):
        return '{0}.{1}{2}'.format(
            self.task.hive['db'],
            self.task.hive['table_prefix'],
            self.table.name)

    def _arg_column_map(self, layer):
        type_mapping = self.task.map_types.get(layer, {})
        mapped_columns = ["{0}={1}".format(c.name, type_mapping[c.type])
                          for c in self.columns if c.type in type_mapping]
        return ','.join(mapped_columns) if mapped_columns else False

    def args(self):
        """ Get arguments of the Sqoop command for this task as dictionary"""
        basic_args = {
            'connect': self._arg_jdbc_url(),
            'username': self.task.source['user'],
            'table': self.table.name,
            'hive-import': True,
            'map-column-hive': self._arg_column_map('hive'),
            'map-column-java': self._arg_column_map('java'),
            'hive-table': self._arg_hive_tablename()
        }

        if 'password' in self.task.source:
            basic_args['password'] = "'" + self.task.source['password'] + "'"
        else:
            basic_args['password-file'] = self.task.source['password_file']

        custom_args = self.task.sqoop_args(self.table)
        return merge_dict(custom_args, basic_args)

    @staticmethod
    def _arg2str(k, v):
        prefix = '-' if len(k) == 1 else '--'
        value = '' if isinstance(v, bool) else v
        return '{0}{1} {2}'.format(prefix, k, value).strip()

    def as_string(self):
        args = {
            SqoopCmd._arg2str(k, v)
            for k, v in self.args().iteritems()
            if v}

        prefix = self.task.script['prefix']
        command = ' '.join(['sqoop'] +
                           self._arg_jvmargs() +
                           ['import']) + ' \\\n   '
        postfix = self.task.script['postfix']
        return prefix + \
               command + ' \\\n   '.join(sorted(args)) + ' ' + \
               postfix + '\n'
