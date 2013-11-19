from django.db import models

from django.db import connections

class SQLCountIf(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'COUNT'
    sql_template= '%(function)s(CASE %(condition)s WHEN true THEN 1 ELSE NULL END)'

class CountIf(models.Aggregate):
    name = 'COUNT'

    def add_to_query(self, query, alias, col, source, is_summary):
        sql, params = query.model._default_manager.filter(**self.extra['condition']).query.where.as_sql(None, None)
        for search, replace in self.extra.get('sql_replace', {}).items():
            sql = sql.replace(search, replace)
        self.extra['condition'] = sql % tuple(params)
        aggregate = SQLCountIf(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate

class SQLSumIf(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'SUM'
    sql_template= '%(function)s(CASE %(condition)s WHEN true THEN %(sum_column)s ELSE NULL END)'

class SumIf(models.Aggregate):
    name = 'SUM'

    def add_to_query(self, query, alias, col, source, is_summary):
        raise Exception, query.where.connector
        connection = connections[query.db]
        sql, params = query.model._default_manager.filter(**self.extra['condition']).query.where.as_sql(qn=None, connection=connection)
        for search, replace in self.extra.get('sql_replace', {}).items():
            sql = sql.replace(search, replace)
        self.extra['condition'] = sql % tuple(params)
        aggregate = SQLSumIf(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate
