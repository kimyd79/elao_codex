"""Four bounded, database-aggregated access-log checks; no external AI calls."""
import logging
import math
import time
from datetime import timedelta
from statistics import median

from django.db import connections
from django.db.models import Aggregate, Avg, Count, FloatField, IntegerField, Max, Min, Q
from django.db.models.expressions import RawSQL
from django.shortcuts import get_object_or_404

from .ai_dataset import authorize, bucket_expression, prepare_queryset, validate_filter
from .models import LogFile, LogMaster


logger = logging.getLogger(__name__)

TRAFFIC_HISTORY_BUCKETS = 3
TRAFFIC_SPIKE_FACTOR = 3
TRAFFIC_MIN_REQUESTS = 100


class Percentile(Aggregate):
    function = 'PERCENTILE_CONT'
    template = '%(function)s(%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s)'
    output_field = FloatField()

    def __init__(self, expression, percentile):
        super().__init__(expression, percentile=percentile)


def measured_format(file):
    fmt = file.file_format or ''
    return any(token in fmt for token in ('%D', '%T', '$request_time', 'time-taken'))


def changes(timeline, key, rate=False):
    """Compare full buckets with preceding 3–5 full buckets, including zeroes."""
    found = []
    for i, current in enumerate(timeline):
        history = timeline[max(0, i - 5):i]
        if len(history) < 3 or current['partial'] or any(p['partial'] for p in history):
            continue
        if rate:
            base = median(p[key] / max(p['requests'], 1) for p in history)
            value = current[key] / max(current['requests'], 1)
            hit = current['requests'] >= 20 and current[key] >= 5 and value >= base + .1
        else:
            base = median(p[key] for p in history)
            value = current[key]
            hit = value >= max(20, base * 3)
        if hit:
            found.append(dict(start=current['start'], end=current['end'], baseline=base,
                              observed=value, count=current[key]))
    return found


def traffic_spikes(timeline):
    """Find traffic buckets at least 3x the preceding three-bucket median."""
    found = []
    for i, current in enumerate(timeline):
        history = timeline[i - TRAFFIC_HISTORY_BUCKETS:i]
        if (i < TRAFFIC_HISTORY_BUCKETS or current['partial']
                or any(point['partial'] for point in history)):
            continue
        base = median(point['requests'] for point in history)
        value = current['requests']
        if value >= TRAFFIC_MIN_REQUESTS and value >= base * TRAFFIC_SPIKE_FACTOR:
            found.append(dict(start=current['start'], end=current['end'], baseline=base,
                              observed=value, count=value))
    return found


def operational_bucket_expression(queryset, start, ranges):
    """Return a constant-size 60-second bucket expression on PostgreSQL.

    The fallback keeps tests and non-PostgreSQL installations compatible. It
    must not be used for large ranges because its SQL grows with every bucket.
    """
    if connections[queryset.db].vendor == 'postgresql':
        return RawSQL(
            "FLOOR(EXTRACT(EPOCH FROM (TO_TIMESTAMP(fdatetime, 'YYYYMMDDHH24MISS') "
            "- %s::timestamp)) / 60)::integer",
            [start], output_field=IntegerField(),
        )
    return bucket_expression(ranges)


def analyze(queryset, files, start, end):
    started = time.perf_counter()
    queryset = queryset.order_by()
    total = queryset.count()
    duration = int((end - start).total_seconds()) + 1
    step = 60
    ranges = {}
    bucket_count = math.ceil(duration / step)
    # The CASE fallback grows linearly with the selected range. PostgreSQL uses
    # a constant-size expression, so it needs no eagerly materialized ranges.
    if connections[queryset.db].vendor != 'postgresql':
        for i in range(bucket_count):
            left = start + timedelta(seconds=i * step)
            ranges[str(i)] = (left, min(end + timedelta(seconds=1), left + timedelta(seconds=step)))
    bucket = operational_bucket_expression(queryset, start, ranges)
    buckets = {}
    timeline_started = time.perf_counter()
    for row in queryset.annotate(bucket=bucket).values('bucket').annotate(
            requests=Count('pk'), server_errors=Count('pk', filter=Q(fstatus__startswith='5')),
            not_found=Count('pk', filter=Q(fstatus='404'))):
        index = row.pop('bucket')
        if index is None or not 0 <= index < bucket_count:
            logger.warning('Operational findings ignored out-of-range bucket: model=%s bucket=%r',
                           queryset.model._meta.db_table, index)
            continue
        buckets[index] = row
    logger.info('Operational findings timeline aggregated: model=%s rows=%d buckets=%d elapsed=%.3fs',
                queryset.model._meta.db_table, total, bucket_count, time.perf_counter()-timeline_started)

    def point(index):
        left = start + timedelta(seconds=index * step)
        right = min(end + timedelta(seconds=1), left + timedelta(seconds=step))
        value = dict(start=left.isoformat(), end=right.isoformat(),
                     partial=(right-left).total_seconds() < step,
                     requests=0, server_errors=0, not_found=0)
        value.update(buckets.get(index, {}))
        return value

    def sparse_changes(key, rate=False):
        found = []
        for i in sorted(buckets):
            current = point(i)
            history = [point(j) for j in range(max(0, i-5), i)]
            if len(history) < 3 or current['partial'] or any(p['partial'] for p in history):
                continue
            if rate:
                base = median(p[key] / max(p['requests'], 1) for p in history)
                value = current[key] / max(current['requests'], 1)
                hit = current['requests'] >= 20 and current[key] >= 5 and value >= base + .1
            else:
                base = median(p[key] for p in history)
                value = current[key]
                hit = value >= max(20, base * 3)
            if hit:
                found.append(dict(start=current['start'], end=current['end'], baseline=base,
                                  observed=value, count=current[key]))
        return found

    def sparse_traffic_spikes():
        found = []
        for i in sorted(buckets):
            current = point(i)
            if (i < TRAFFIC_HISTORY_BUCKETS
                    or current['requests'] < TRAFFIC_MIN_REQUESTS or current['partial']):
                continue
            history = [point(j) for j in range(i-TRAFFIC_HISTORY_BUCKETS, i)]
            base = median(p['requests'] for p in history)
            if current['requests'] >= base * TRAFFIC_SPIKE_FACTOR:
                found.append(dict(start=current['start'], end=current['end'], baseline=base,
                                  observed=current['requests'], count=current['requests']))
        return found

    def top(query, fields, **aggregates):
        return list(query.values(*fields).annotate(count=Count('pk'), **aggregates)
                    .order_by('-count', *fields)[:10])

    ips = top(queryset.exclude(fip__in=['', '-', 'NA']).exclude(fip__isnull=True), ['fip'])
    requests = top(queryset, ['frequest'])
    def concentration(rows):
        return [dict(row, share=round(row['count'] / max(total, 1) * 100, 2))
                for row in rows if row['count'] >= 20 and row['count'] / max(total, 1) >= .5]
    concentrated = concentration(ips)
    concentrated_requests = concentration(requests)
    spikes = sparse_traffic_spikes()
    measured_ids = [f.logfile_id for f in files if measured_format(f)]
    measured = queryset.filter(logfile_id__in=measured_ids, ftime_taken__gte=0)
    performance = measured.aggregate(count=Count('pk'), avg_ms=Avg('ai_ms'), max_ms=Max('ai_ms'),
                                     p95_ms=Percentile('ai_ms', .95), p99_ms=Percentile('ai_ms', .99),
                                     slow=Count('pk', filter=Q(ai_ms__gte=1000)))
    slow_urls = list(measured.values('frequest').annotate(count=Count('pk'), avg_ms=Avg('ai_ms'),
                     p95_ms=Percentile('ai_ms', .95), p99_ms=Percentile('ai_ms', .99),
                     slow=Count('pk', filter=Q(ai_ms__gte=1000)))
                     .filter(slow__gt=0).order_by('-slow', 'frequest')[:10])
    durations = {row['bucket']: row for row in measured.annotate(bucket=bucket)
                 .values('bucket').annotate(count=Count('pk'), avg_ms=Avg('ai_ms'))}
    latency_changes = []
    for i in sorted(durations):
        current_point = point(i)
        history = [point(j) for j in range(max(0, i-5), i)]
        previous = [durations.get(j) for j in range(max(0, i-5), i)]
        current = durations.get(i)
        if (len(history) < 3 or current_point['partial'] or any(p['partial'] for p in history)
                or not current or current['count'] < 20 or any(p is None for p in previous)):
            continue
        baseline = median(p['avg_ms'] for p in previous)
        if current['avg_ms'] >= max(baseline * 3, baseline + 100):
            latency_changes.append(dict(start=current_point['start'], end=current_point['end'],
                                        baseline=baseline, observed=current['avg_ms'], count=current['count']))
    errors = queryset.filter(fstatus__startswith='5')
    missing = queryset.filter(fstatus='404')
    error_count, missing_count = errors.count(), missing.count()
    error_changes = sparse_changes('server_errors', True)
    missing_changes = sparse_changes('not_found', True)

    def card(key, title, detected, available, evidence, rule, guidance):
        return dict(id=key, title=title, status=('insufficient' if not available else 'detected' if detected else 'clear'),
                    evidence=evidence, rule=rule, guidance=guidance)

    result = dict(total=total, scope=dict(start=start.isoformat(), end=end.isoformat(), bucket_seconds=step),
        findings=[
            card('traffic', '트래픽 급증·집중', bool(spikes or concentrated or concentrated_requests), total > 0,
                 dict(spikes=spikes[:10], spike_count=len(spikes), concentrated_ips=concentrated,
                      concentrated_requests=concentrated_requests),
                 '60초 구간에서 100건 이상이고 직전 3개 완전 구간의 중앙값 대비 3배 이상. IP·요청 집중은 20건 이상·전체의 50% 이상.',
                 ['이벤트·배치·프록시 공유 IP로 인한 정상 집중인지 확인하세요.',
                  '집중 IP와 URL을 확인한 후 요청 제한·캐시 적용·서버 용량 조정을 검토하세요.']),
            card('performance', '응답 지연·성능 저하', bool(performance['slow'] or latency_changes), performance['count'] > 0,
                 dict(**performance, excluded=total-performance['count'], slow_urls=slow_urls,
                      latency_changes=latency_changes[:10], latency_change_count=len(latency_changes)),
                 '실측 필드만 ms로 환산. 1,000ms 이상 요청·p95·p99를 계산합니다. 지연 증가: 20건 이상 구간의 평균이 직전 3~5구간 대비 3배 이상·100ms 이상 상승.',
                 ['느린 URL의 DB 쿼리·외부 API·서버 자원을 같은 시간대의 애플리케이션 로그와 대조하세요.',
                  '응답시간 필드가 없는 파일은 성능 분석에서 제외됩니다. 로그 포맷에 처리시간을 추가하세요.']),
            card('server_errors', '서버 오류 증가', error_count > 0, total > 0,
                 dict(count=error_count, rate=error_count/max(total, 1)*100, increases=error_changes[:10],
                      increase_count=len(error_changes), top_urls=top(errors, ['frequest', 'fstatus']),
                      top_ips=top(errors, ['fip'])),
                 '5xx 발생을 표시. 증가 후보는 구간 요청 20건·오류 5건 이상이며 직전 3~5구간 대비 오류율 10%p 이상 상승.',
                 ['발생 URL·상태코드·시간대를 배포 이력 및 애플리케이션 오류 로그와 대조하세요.',
                  '502·503·504는 upstream 연결·가용 인스턴스·타임아웃을 확인하고 배포 관련이면 롤백을 검토하세요.']),
            card('not_found', '404 경로·링크 오류', missing_count > 0, total > 0,
                 dict(count=missing_count, rate=missing_count/max(total, 1)*100, increases=missing_changes[:10],
                      increase_count=len(missing_changes), top_urls=top(missing, ['frequest']),
                      referrers=top(missing, ['frequest', 'freferer'])),
                 '404 발생 URL·Referer를 집계. 증가 후보는 구간 요청 20건·404 5건 이상, 비율 10%p 이상 상승.',
                 ['상위 404 URL과 Referer를 확인해 깨진 링크·정적 파일 누락·삭제된 API 호출을 구분하세요.',
                  '라우팅·배포 파일·호출 경로를 수정하거나 필요한 리다이렉트를 추가하세요. 탐색 봇 여부도 확인하세요.']),
        ], limitations=[
            '검출 결과는 확인이 필요한 후보이며 장애·공격을 확정하지 않습니다.',
            '기준선은 선택 구간 내부만 사용합니다. 과거 같은 요일·시간대와 비교하지 않습니다.',
            '요청·URL은 원본 요청 문자열로 집계하며 쿼리·리소스 ID가 다르면 별도 그룹입니다.',
            '0건 구간은 트래픽 부재와 로그 누락을 구분할 수 없습니다. 마지막 불완전 구간은 증가 판단에서 제외합니다.',
            '상세 순위·증가 구간은 각각 최대 10개입니다. 백분위수는 표본이 아닌 선택된 실측 로그 전체 기준입니다.',
        ])
    logger.info('Operational findings analysis completed: model=%s rows=%d buckets=%d elapsed=%.3fs',
                queryset.model._meta.db_table, total, bucket_count, time.perf_counter()-started)
    return result


def build_findings(user, project_id, data):
    from dynamic_models.models import ModelSchema
    project = get_object_or_404(LogMaster, pk=project_id)
    authorize(user, project)
    files = list(LogFile.objects.filter(project=project))
    schema = get_object_or_404(ModelSchema, name='logdetail_' + str(project.pk))
    query = schema.as_model().objects.filter(logfile_id__in=[f.pk for f in files]).order_by()
    data = dict(data)
    bounds = query.aggregate(first=Min('fdatetime'), last=Max('fdatetime'))
    first, last = bounds['first'] or '20000101000000', bounds['last'] or '20000101000000'
    for key, default in [('dateFromValue', first[:8]), ('timeFromValue', first[8:]),
                         ('dateToValue', last[:8]), ('timeToValue', last[8:])]:
        data[key] = data.get(key) or default
    if 'projectServers' not in data:
        data['projectServers'] = [f'{f.server_name or "-"}-{f.instance_name or "-"}' for f in files]
    filters = validate_filter(str(project.pk), data)
    # Exclude estimated durations when a response-time filter is requested too.
    query = prepare_queryset(query, files, filters)
    if filters['lower_ms'] is not None or filters['upper_ms'] is not None:
        query = query.filter(logfile_id__in=[f.pk for f in files if measured_format(f)], ftime_taken__gte=0)
        # Match Search's exclusive one-sided and inclusive two-sided bounds.
        if filters['lower_ms'] is None:
            query = query.filter(ai_ms__lt=filters['upper_ms'])
        elif filters['upper_ms'] is None:
            query = query.filter(ai_ms__gt=filters['lower_ms'])
    return analyze(query, files, filters['start'], filters['end'])
