from contextlib import contextmanager

from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager


MYSQL_CREDENTIALS_CONTRACT = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'database': {
            'type': 'string',
        },
        'host': {
            'type': 'string',
        },
        'user': {
            'type': 'string',
        },
        'password': {
            'type': 'string',
        },
        'port': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 65535,
        },
    },
    'required': ['database', 'host', 'user', 'password', 'port']
}


class MySQLCredentials(Credentials):
    SCHEMA = MYSQL_CREDENTIALS_CONTRACT

    @property
    def type(self):
        return 'mysql'

    def _connection_keys(self):
        return ('host', 'port', 'user', 'database')


class MySQLConnectionManager(SQLConnectionManager):
    TYPE = 'mysql'
