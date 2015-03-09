
from cornet.connectors.base_connector import BaseConnector


def test_get_password_from_string():
    source = {'password': '123'}
    assert BaseConnector(source)._get_password() == '123'


def test_get_password_from_file():
    source = {'password_file': 'tests/configs/password'}
    assert BaseConnector(source)._get_password() == 'my-secret-password-123'
