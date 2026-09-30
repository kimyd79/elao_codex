import hashlib

from django.db import connection


# Keep text-heavy request/referrer/user-agent columns out of B-tree indexes:
# real access logs can exceed PostgreSQL's per-index-entry size limit. These
# compact columns cover the common statistics filters and low-cardinality
# GROUP BY operations without duplicating the large raw payload.
STATISTICS_INDEXES = (
    ('datetime', (('fdatetime', ''), ('logfile_id', ''))),
    ('status', (('fstatus', ''), ('logfile_id', ''))),
    ('ip', (('fip', ''), ('logfile_id', ''))),
    ('extension', (('fextension', ''), ('logfile_id', ''))),
    ('time_taken', (('ftime_taken', 'DESC'), ('logfile_id', ''))),
    ('upstream', (('freserve1', ''), ('logfile_id', ''))),
    ('domain', (('freserve2', ''), ('logfile_id', ''))),
)


def statistics_index_statements(table_name, concurrently=False):
    quote = connection.ops.quote_name
    table_token = hashlib.sha1(table_name.encode('utf-8')).hexdigest()[:10]
    concurrent_sql = ' CONCURRENTLY' if concurrently and connection.vendor == 'postgresql' else ''
    statements = []
    for suffix, columns in STATISTICS_INDEXES:
        index_name = 'elao_stat_%s_%s' % (table_token, suffix)
        column_sql = ', '.join(
            '%s%s' % (quote(column), ' ' + direction if direction else '')
            for column, direction in columns
        )
        statements.append(
            'CREATE INDEX%s IF NOT EXISTS %s ON %s (%s)'
            % (concurrent_sql, quote(index_name), quote(table_name), column_sql)
        )
    return statements


def ensure_statistics_indexes(model, concurrently=False):
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        for statement in statistics_index_statements(table_name, concurrently):
            cursor.execute(statement)
        cursor.execute('ANALYZE %s' % connection.ops.quote_name(table_name))

