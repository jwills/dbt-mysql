from dbt.adapters.dbt-mysql.connections import MySQLConnectionManager
from dbt.adapters.dbt-mysql.connections import MySQLCredentials
from dbt.adapters.dbt-mysql.impl import MySQLAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import dbt-mysql


Plugin = AdapterPlugin(
    adapter=MySQLAdapter,
    credentials=MySQLCredentials,
    include_path=dbt-mysql.PACKAGE_PATH)
