from dbt.adapters.sql import SQLAdapter
from dbt.adapters.mysql import MySQLColumn, MySQLConnectionManager

class MySQLAdapter(SQLAdapter):
    ConnectionManager = MySQLConnectionManager
    Column = MySQLColumn

    @classmethod
    def date_function(cls):
        return 'now()'
