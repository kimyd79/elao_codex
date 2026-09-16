"""Read-only AI evidence builder. No network client or public endpoint.

Call build_project_dataset with an authenticated user, never a client queryset.
All heavy aggregation stays in the database; only bounded groups/samples return.
"""
import json
import math
import time
from datetime import datetime, timedelta
from statistics import median
from uuid import UUID

from django.db import connection, transaction
from django.db.models import Avg, Case, Count, F, FloatField, IntegerField, Max, Q, Value, When, Window
from django.db.models.functions import RowNumber
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, ValidationError

STAMP = '%Y%m%d%H%M%S'
FIELDS = {'I': 'fip', 'R': 'frequest', 'E': 'freferer', 'U': 'fuser_agent', 'S': 'fstatus'}


def validate_filter(project_id, data):
    try:
        project_id = str(UUID(str(project_id)))
        if data.get('project_id') and str(UUID(str(data['project_id']))) != project_id:
            raise ValueError('Conflicting project IDs')
        start = datetime.strptime(data['dateFromValue'] + data['timeFromValue'], STAMP)
        end = datetime.strptime(data['dateToValue'] + data['timeToValue'], STAMP)
        if start > end:
            raise ValueError('Reversed date range')
        servers = data.get('projectServers', [])
        if not isinstance(servers, list) or not all(isinstance(s, str) for s in servers):
            raise ValueError('projectServers must be an array')
        condition = data.get('conditionValue') or 'N'
        if condition not in {'N', *FIELDS}:
            raise ValueError('Unknown condition')
        exclude = data.get('excludeSearch', False)
        if exclude not in (True, False, 'true', 'false', ''):
            raise ValueError('Invalid exclude flag')
        bounds = [None if data.get(k) in (None, '') else float(data[k])
                  for k in ('ttFromValue', 'ttToValue')]
        if any(v is not None and (not math.isfinite(v) or v < 0) for v in bounds):
            raise ValueError('Invalid response time')
        if all(v is not None for v in bounds) and bounds[0] > bounds[1]:
            raise ValueError('Reversed response time')
        keyword = data.get('searchValue') or ''
        if not isinstance(keyword, str) or len(keyword) > 1000:
            raise ValueError('Invalid keyword')
    except (ValueError, TypeError, KeyError) as exc:
        raise ValidationError(str(exc)) from exc
    return dict(project_id=project_id, start=start, end=end, servers=servers,
                condition=condition, keyword=keyword, exclude=exclude in (True, 'true'),
                lower_ms=bounds[0], upper_ms=bounds[1])


def authorize(user, project):
    if not user or not user.is_authenticated:
        raise NotAuthenticated()
    if not (user.is_staff or user.is_superuser or project.creator == user.username):
        raise PermissionDenied('Project access denied')


def prepare_queryset(queryset, files, filters):
    # Match the stored server-instance label as a whole (names may contain '-').
    selected = [f for f in files if f'{f.server_name or "-"}-{f.instance_name or "-"}' in filters['servers']]
    # Match current storage convention: %T seconds, other formats microseconds.
    seconds = [str(f.logfile_id) for f in selected
               if '%T' in f.file_format and '%D' not in f.file_format]
    queryset = queryset.filter(logfile_id__in=[f.logfile_id for f in selected]).annotate(
        ai_ms=Case(When(logfile_id__in=seconds, then=F('ftime_taken') * Value(1000.0)),
                   default=F('ftime_taken') / Value(1000.0), output_field=FloatField()))
    queryset = queryset.filter(fdatetime__gte=filters['start'].strftime(STAMP),
                               fdatetime__lte=filters['end'].strftime(STAMP))
    field = FIELDS.get(filters['condition'])
    if field and filters['keyword']:
        clause = {field + '__icontains': filters['keyword']}
        queryset = queryset.exclude(**clause) if filters['exclude'] else queryset.filter(**clause)
    for bound, lookup in [('lower_ms', 'ai_ms__gte'), ('upper_ms', 'ai_ms__lte')]:
        if filters[bound] is not None:
            queryset = queryset.filter(**{lookup: filters[bound]})
    return queryset.order_by()


def metric_expressions():
    return dict(requests=Count('pk'),
        unique_ips=Count('fip', distinct=True, filter=~Q(fip__in=['', '-'])),
        errors=Count('pk', filter=Q(fstatus__startswith='4') | Q(fstatus__startswith='5')),
        avg_ms=Avg('ai_ms'), max_ms=Max('ai_ms'))


def metrics(queryset):
    return queryset.aggregate(**metric_expressions())


def bucket_expression(ranges):
    return Case(*[When(fdatetime__gte=left.strftime(STAMP),
        fdatetime__lt=right.strftime(STAMP), then=Value(i))
        for i, (left, right) in enumerate(ranges.values())], output_field=IntegerField())


def top(queryset, fields):
    return list(queryset.values(*fields).annotate(count=Count('pk')).order_by('-count', *fields)[:10])


def detect_candidates(timeline):
    found = []
    for i, point in enumerate(timeline):
        history = timeline[max(0, i - 5):i]
        if len(history) < 3 or point['partial'] or any(p['partial'] for p in history):
            continue
        reasons = []
        for key in ('requests', 'unique_ips'):
            base = median(p[key] for p in history)
            value = point[key]
            if max(base, value) >= 20 and (value >= max(20, base * 3) or (base >= 20 and value <= base * .3)):
                reasons.append(dict(metric=key, baseline=base, observed=value))
        base_error = median(p['errors'] / max(p['requests'], 1) for p in history)
        error_rate = point['errors'] / max(point['requests'], 1)
        if point['requests'] >= 20 and point['errors'] >= 5 and error_rate - base_error >= .1:
            reasons.append(dict(metric='error_rate', baseline=base_error, observed=error_rate))
        times = [p['avg_ms'] for p in history if p['avg_ms'] is not None]
        if times and point['requests'] >= 20 and point['avg_ms'] is not None:
            base = median(times)
            if point['avg_ms'] >= max(base * 3, base + 100):
                reasons.append(dict(metric='avg_ms', baseline=base, observed=point['avg_ms']))
        if reasons:
            found.append(dict(bucket_id=point['id'], reasons=reasons, history_buckets=len(history)))
    return found


def entity_candidates(queryset, timeline, ranges):
    """Bounded per-bucket leaders, followed by exact counts including zeroes.

    Never treat exclusion from a top-N list as a zero observation.
    """
    bucket_expr = bucket_expression(ranges)
    output, coverage = [], {}
    for field in ('fip', 'frequest'):
        grouped = queryset.exclude(**{field + '__isnull': True}).exclude(
            **{field + '__in': ['', '-']}).annotate(ai_bucket=bucket_expr)
        leaders = list(grouped.values('ai_bucket', field).annotate(n=Count('pk')).annotate(
            rank=Window(RowNumber(), partition_by=[F('ai_bucket')],
                        order_by=[F('n').desc(), F(field).asc()])).filter(rank__lte=10))
        peaks = {}
        for row in leaders:
            peaks[row[field]] = max(peaks.get(row[field], 0), row['n'])
        tracked = sorted(peaks, key=lambda value: (-peaks[value], value))[:200]
        coverage[field] = dict(per_bucket_top=10, discovered=len(peaks), tracked=len(tracked),
                               truncated=len(peaks) > len(tracked))
        series = {value: [0] * len(timeline) for value in tracked}
        rows = grouped.filter(**{field + '__in': tracked}).values('ai_bucket', field).annotate(n=Count('pk'))
        # At most 200 entities x 120 buckets. Avoid a server-side cursor whose
        # FETCH calls bypass the per-execute deadline wrapper.
        for row in rows:
            series[row[field]][row['ai_bucket']] = row['n']
        for value, counts in series.items():
            for i in range(3, len(timeline)):
                history = timeline[max(0, i-5):i]
                if timeline[i]['partial'] or any(p['partial'] for p in history):
                    continue
                baseline = median(counts[max(0, i-5):i])
                observed = counts[i]
                up = observed >= max(20, baseline * 3)
                down = baseline >= 20 and observed <= baseline * .3
                if up or down:
                    output.append(dict(bucket_id=timeline[i]['id'], field=field, value=value,
                        direction='increase' if up else 'decrease', baseline=baseline, observed=observed,
                        current_share=observed/max(timeline[i]['requests'], 1),
                        history_counts=counts[max(0, i-5):i],
                        baseline_method='median of preceding 3-5 full buckets'))
    output.sort(key=lambda row: (-abs(row['observed']-row['baseline']), row['bucket_id'], row['field'], row['value']))
    return output[:100], dict(fields=coverage, candidate_count=len(output), returned=min(100, len(output)))


def build_dataset(queryset, filters):
    """Internal helper: queryset must already be authorized and filtered."""
    start, end = filters['start'], filters['end'] + timedelta(seconds=1)
    duration = int((end - start).total_seconds())
    step = next((s for s in (1, 10, 60, 300, 900, 3600, 21600, 86400)
                 if math.ceil(duration / s) <= 120), math.ceil(duration / 120))
    timeline, ranges = [], {}
    for i in range(math.ceil(duration / step)):
        left, right = start + timedelta(seconds=i * step), min(end, start + timedelta(seconds=(i + 1) * step))
        key = f'b{i}'
        ranges[key] = (left, right)
        timeline.append(dict(id=key, start=left.isoformat(), end_exclusive=right.isoformat(),
                             partial=(right-left).total_seconds() < step,
                             requests=0, unique_ips=0, errors=0, avg_ms=None, max_ms=None))
    grouped = queryset.annotate(ai_bucket=bucket_expression(ranges)).values('ai_bucket').annotate(**metric_expressions())
    for row in grouped:
        index = row.pop('ai_bucket')
        timeline[index].update(row)
    candidates = detect_candidates(timeline)
    entity_changes, entity_coverage = entity_candidates(queryset, timeline, ranges)
    by_bucket = {c['bucket_id']: c for c in candidates}
    for change in entity_changes:
        candidate = by_bucket.setdefault(change['bucket_id'], dict(bucket_id=change['bucket_id'], reasons=[],
                                             history_buckets=len(change['history_counts'])))
        candidate['reasons'].append(dict(metric=change['field'], entity=change['value'],
            baseline=change['baseline'], observed=change['observed']))
    candidates = list(by_bucket.values())
    details = []
    for candidate in candidates[:5]:
        left, right = ranges[candidate['bucket_id']]
        current = queryset.filter(fdatetime__gte=left.strftime(STAMP), fdatetime__lt=right.strftime(STAMP))
        previous = queryset.filter(fdatetime__gte=(left-timedelta(seconds=step)).strftime(STAMP), fdatetime__lt=left.strftime(STAMP))
        entities = {}
        for label, fields in [('ips', ['fip']), ('requests', ['frequest']), ('ip_requests', ['fip', 'frequest'])]:
            # Include previous leaders to expose entities that disappeared.
            leaders = top(current, fields) + top(previous, fields)
            unique = {tuple(row[f] for f in fields) for row in leaders}
            selector = Q(pk__in=[])
            for values in unique:
                selector |= Q(**dict(zip(fields, values)))
            def counts(query):
                return {tuple(row[f] for f in fields): row['count'] for row in
                        query.filter(selector).values(*fields).annotate(count=Count('pk'))}
            current_counts, previous_counts = counts(current), counts(previous)
            entities[label] = [dict(zip(fields, values), current_count=current_counts.get(values, 0),
                                   previous_count=previous_counts.get(values, 0))
                               for values in sorted(unique, key=str)]
        details.append(dict(**candidate, entities=entities, baseline='previous equal-duration bucket'))
    fields = ['pk', 'logfile_id', 'fdatetime', 'fip', 'frequest', 'fstatus', 'ai_ms', 'log_line']
    samples = {}
    groups = [('time_start', queryset.order_by('fdatetime', 'pk')),
              ('time_end', queryset.order_by('-fdatetime', 'pk')),
              ('errors', queryset.filter(Q(fstatus__startswith='4') | Q(fstatus__startswith='5')).order_by('fdatetime', 'pk')),
              ('slow', queryset.filter(ai_ms__isnull=False).order_by('-ai_ms', 'pk'))]
    for detail in details:
        left, right = ranges[detail['bucket_id']]
        groups.append((detail['bucket_id'], queryset.filter(fdatetime__gte=(left-timedelta(seconds=step)).strftime(STAMP),
                      fdatetime__lt=(right+timedelta(seconds=step)).strftime(STAMP)).order_by('fdatetime', 'pk')))
    for label, group in groups:
        for row in group.values(*fields)[:20]:
            key = str(row.pop('pk'))
            row['logfile_id'] = str(row['logfile_id'])
            row['log_line'] = (row['log_line'] or '')[:2000]
            if key not in samples:
                samples[key] = dict(id='row:' + key, reasons=[label], **row)
            elif label not in samples[key]['reasons']:
                samples[key]['reasons'].append(label)
    result = dict(schema_version=1, scope=dict(project_id=filters['project_id'], start=start.isoformat(),
        end_inclusive=filters['end'].isoformat(), timezone='unknown', response_time_unit='ms',
        applied_filter={k:v for k,v in filters.items() if k not in ('start','end')}),
        summary=metrics(queryset), bucket_seconds=step, timeline=timeline,
        candidates=candidates, entity_changes=entity_changes, entity_coverage=entity_coverage,
        details=details, samples=list(samples.values())[:200],
        limitations=['Unique IPs are not people.', 'Zero counts cannot distinguish no traffic from missing logs.',
                      'Heuristic candidates, not confirmed incidents; no historical baseline outside selected range.',
                      'Request groups preserve full request strings; path normalization is not yet applied.',
                      'Stored zero response times may include parser defaults. Percentiles not included.',
                      'At most five candidate buckets have entity details; samples are intentionally biased.',
                      'Entity detection tracks per-bucket top 10, capped at 200 entities per field and 100 changes.'],
        sampling=dict(max_rows=200, truncated=False))
    encode = lambda: json.dumps(result, ensure_ascii=False, allow_nan=False).encode('utf-8')
    while len(encode()) > 128 * 1024 - 64 and result['samples']:
        result['samples'].pop()
        result['sampling']['truncated'] = True
    while len(encode()) > 128 * 1024 - 64 and result['details']:
        result['details'].pop()
        result['sampling']['truncated'] = True
    if len(encode()) > 128 * 1024:
        raise ValidationError('Evidence exceeds input budget')
    result['sampling']['count'] = len(result['samples'])
    return result


def build_project_dataset(user, project_id, data):
    from dynamic_models.models import ModelSchema
    from .models import LogMaster, LogFile
    if not user or not user.is_authenticated:
        raise NotAuthenticated()
    filters = validate_filter(project_id, data)
    # Must own the outer transaction so PostgreSQL snapshot setup precedes reads.
    if connection.in_atomic_block:
        raise RuntimeError('Dataset builder requires an outermost transaction')
    deadline = time.monotonic() + 60
    def enforce_budget(execute, sql, params, many, context):
        if time.monotonic() > deadline:
            raise TimeoutError('AI dataset exceeded 60-second query budget')
        return execute(sql, params, many, context)
    # Checked between statements; an in-flight statement has its own 15s limit.
    with connection.execute_wrapper(enforce_budget), transaction.atomic():
        if connection.vendor == 'postgresql':
            with connection.cursor() as cursor:
                cursor.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY')
                cursor.execute("SET LOCAL statement_timeout = '15000ms'")
                # Generated bucket CASE expressions are expensive to JIT;
                # these bounded analytical reads do not amortize compilation.
                cursor.execute('SET LOCAL jit = off')
        project = LogMaster.objects.get(pk=filters['project_id'])
        authorize(user, project)
        files = list(LogFile.objects.filter(project=project))
        model = ModelSchema.objects.get(name='logdetail_' + filters['project_id']).as_model()
        return build_dataset(prepare_queryset(model.objects.all(), files, filters), filters)
