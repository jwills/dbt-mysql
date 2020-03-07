from dataclasses import dataclass
from typing import Optional

from dbt.adapters.base import Column
from dbt.adapters.base.relation import BaseRelation, Policy

@dataclass
class MySQLIncludePolicy(Policy):
    database: bool = True
    schema: bool = False
    identifier: bool = True

class MySQLQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False

@dataclass(frozen=True, eq=False, repr=False)
class MySQLRelation(BaseRelation):
    quote_character: str = '`'
    include_policy: MySQLIncludePolicy = MySQLIncludePolicy()
    quote_policy: MySQLQuotePolicy = MySQLQuotePolicy()

@dataclass
class MySQLColumn(Column):
    @property
    def quoted(self) -> str:
        return '`{}`'.format(self.column)
