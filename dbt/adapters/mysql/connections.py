from contextlib import contextmanager

import MySQLdb

import dbt
from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.logger import GLOBAL_LOGGER as logger


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
    ALIASES = {
      'db': 'database',
      'passwd': 'password',
    }

    @property
    def type(self):
        return 'mysql'

    def _connection_keys(self):
        return ('host', 'port', 'user', 'database')


class MySQLConnectionManager(SQLConnectionManager):
    TYPE = 'mysql'

    @contextmanager
    def exception_handler(self, sql, connection_name='master'):
        try:
            yield
        except MySQLdb.DatabaseError as e:
            logger.debug('MySQL error: {}'.format(str(e)))

            try:
                # attempt to release the connection
                self.release(connection_name)
            except MySQLdb.Error:
                logger.debug("Failed to release connection!")
                pass

            raise dbt.exceptions.DatabaseException(
                dbt.compat.to_string(e).strip())

        except Exception as e:
            logger.debug("Error running SQL: %s", sql)
            logger.debug("Rolling back transaction.")
            self.release(connection_name)
            raise dbt.exceptions.RuntimeException(e)

    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

        base_credentials = connection.credentials
        credentials = cls.get_credentials(connection.credentials.incorporate())

        try:
            handle = MySQLdb.connect(
                dbname=credentials.database,
                user=credentials.user,
                host=credentials.host,
                password=credentials.password,
                port=credentials.port,
                connect_timeout=10)
            
            connection.handle = handle
            connection.state = 'open'
        except MySQLdb.Error as e:
            logger.debug("Got an error when attempting to open a postgres "
                         "connection: '{}'"
                         .format(e))

            connection.handle = None
            connection.state = 'fail'

            raise dbt.exceptions.FailedToConnectException(str(e))

        return connection

    def is_cancelable(self):
        return False

    def cancel(self, connection):
        pass

    @classmethod
    def get_credentials(cls, credentials):
        return credentials

    @classmethod
    def get_status(cls, cursor):
        return cursor.statusmessage
