from sisyphus import main
import pytest


@pytest.mark.parametrize(("k", "v", "exp"), [
    ('delete-target-dir', True, '--delete-target-dir'),
    ('m', 10, '-m 10'),
    ('warehouse-dir', '/user/sqoop2', '--warehouse-dir /user/sqoop2'),
    ('f', True, '-f')])
def test_sqoop_args_to_str(k, v, exp):
    assert main.sqoop_arg_to_str(k, v) == exp
