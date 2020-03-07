from dbt.adapters.sql import SQLAdapter
from dbt.adapters.mysql import MySQLConnectionManager, MySQLRelation

class MySQLAdapter(SQLAdapter):
    ConnectionManager = MySQLConnectionManager
    Relation = MySQLRelation

    @classmethod
    def is_cancelable(cls):
        return False

    @classmethod
    def date_function(cls):
        return 'now()'

    def create_schema(self, database_name, schema_name):
        return 1

    def list_schemas(self, database):
        return [database]

    def check_schema_exists(self, database, schema):
        return database == schema
