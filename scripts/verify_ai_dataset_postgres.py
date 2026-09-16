"""Read-only verification against configured PostgreSQL; no raw log output."""
import os
import json
import time
import sys
from types import SimpleNamespace

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loganalyzer.settings')
sys.stdout.reconfigure(line_buffering=True)
print('Initializing read-only PostgreSQL verification', flush=True)
import django
django.setup()
from django.conf import settings
settings.DATABASES['default'].setdefault('OPTIONS', {})['connect_timeout'] = 10
print('Django initialized', flush=True)

from django.db import connection, transaction
from django.db.models import Min, Max
from dynamic_models.models import ModelSchema
from loganalyzerapi.models import LogMaster, LogFile
from loganalyzerapi.ai_dataset import build_project_dataset, validate_filter, prepare_queryset

if connection.vendor != 'postgresql':
    raise RuntimeError('Expected PostgreSQL')

with transaction.atomic():
    with connection.cursor() as cursor:
        cursor.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY')
        cursor.execute("SET LOCAL statement_timeout = '15000ms'")
        cursor.execute('SHOW transaction_read_only')
        print(json.dumps({'read_only': cursor.fetchone()[0]}))
    projects = list(LogMaster.objects.order_by('-created')[:3])
    targets = []
    for project in projects:
        try:
            model = ModelSchema.objects.get(name='logdetail_' + str(project.pk)).as_model()
        except ModelSchema.DoesNotExist:
            continue
        files = list(LogFile.objects.filter(project=project))
        query = model.objects.filter(logfile_id__in=[f.pk for f in files])
        period = query.aggregate(start=Min('fdatetime'), end=Max('fdatetime'))
        if not period['start'] or not period['end']:
            continue
        data = dict(dateFromValue=period['start'][:8], timeFromValue=period['start'][8:],
                    dateToValue=period['end'][:8], timeToValue=period['end'][8:],
                    projectServers=list({f'{f.server_name or "-"}-{f.instance_name or "-"}' for f in files}))
        expected = prepare_queryset(query, files, validate_filter(project.pk, data)).count()
        targets.append((project, data, expected))
        # EXPLAIN without ANALYZE: inspect access strategy without extra execution.
        plan = json.loads(prepare_queryset(query, files, validate_filter(project.pk, data)).explain(format='json'))
        print(json.dumps({'target': len(targets), 'expected_rows': expected,
                          'plan_node': plan[0]['Plan']['Node Type']}))

if not targets:
    raise RuntimeError('No populated recent dynamic projects available')

for index, (project, data, expected) in enumerate(targets, 1):
    user = SimpleNamespace(is_authenticated=True, username=project.creator, is_staff=False, is_superuser=False)
    statistics = {'queries': 0, 'read_only': None}
    def observe(execute, sql, params, many, context):
        statistics['queries'] += 1
        # No SQL/parameters retained or printed.
        return execute(sql, params, many, context)
    started = time.monotonic()
    with connection.execute_wrapper(observe):
        result = build_project_dataset(user, project.pk, data)
    total = result['summary']['requests']
    assert total == sum(bucket['requests'] for bucket in result['timeline'])
    # Concurrent ingestion could change the separate baseline; expose mismatch.
    assert total == expected, 'Baseline changed or filter mismatch'
    encoded = json.dumps(result, ensure_ascii=False).encode('utf-8')
    assert len(encoded) <= 128 * 1024
    print(json.dumps(dict(target=index, rows=total, seconds=round(time.monotonic()-started, 3),
        queries=statistics['queries'], buckets=len(result['timeline']), samples=len(result['samples']),
        entity_candidates=len(result['entity_changes']), payload_bytes=len(encoded), verified=True)))
