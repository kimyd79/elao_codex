"""Measure the real parser against an uploaded log, using a temporary DB table."""
import os
import sys
import json
import argparse
import time
import tempfile
import uuid
import cProfile
import pstats
import hashlib
from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'EALO' / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loganalyzer.settings')
import django
django.setup()
from loganalyzerapi.models import LogFile

def inventory():
    rows = []
    for item in LogFile.objects.order_by('-created')[:20]:
        path = Path(item.file_object.path)
        rows.append({'id': str(item.pk), 'name': path.name, 'bytes': path.stat().st_size if path.exists() else None,
                     'kind': item.format_kind, 'created': str(item.created)})
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def benchmark(file_id, output, rounds, replay_rejects=False, baseline=None):
    from django.db import connection, transaction
    from django.conf import settings
    from dynamic_models.models import ModelSchema
    from loganalyzerapi.views import DynamicLogDetailViewSet
    from loganalyzerapi.analysis_progress import AnalysisProgress
    from loganalyzerapi.models import LogParseReject
    import pandas as pd
    from loganalyzerapi import parsers

    logfile = LogFile.objects.get(pk=file_id)
    source = Path(logfile.file_object.path)
    if source.suffix.lower() in {'.gz', '.zip'} or logfile.format_kind != 'apache':
        raise ValueError('This measurement harness supports plain Apache logs only')
    if source.stat().st_size > settings.LOG_PARSER_SPLIT_SIZE_BYTES:
        raise ValueError('Use a file below the configured chunk threshold')
    model = ModelSchema.objects.get(name='logdetail_' + str(logfile.project_id)).as_model()
    quote = connection.ops.quote_name
    report = {'file_id': file_id, 'filename': source.name, 'source_bytes': source.stat().st_size,
              'storage_mode': settings.LOG_STORAGE_MODE, 'rounds': [], 'replay_rejects': replay_rejects,
              'method': 'Actual full-file parser; isolated logged PostgreSQL table with copied indexes; COPY transaction rolled back. Progress UPDATE uses a nonexistent job UUID. No production rows changed.'}
    def save():
        Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    for run in range(rounds):
        timings = defaultdict(float)
        phase = [None, time.perf_counter()]
        telemetry = AnalysisProgress(uuid.uuid4())
        class Progress:
            def report(self, name, *args, **kwargs):
                if phase[0] != name:
                    now = time.perf_counter()
                    if phase[0]:
                        timings[phase[0]] += now - phase[1]
                        print(f'Run {run + 1}: {phase[0]} {timings[phase[0]]:.3f}s', flush=True)
                    phase[:] = [name, now]
                telemetry.report(name, *args, **kwargs)
        view = DynamicLogDetailViewSet()
        view.analysis_progress = Progress()
        result = {'run': run + 1}
        print(f'Run {run + 1}: starting full file', flush=True)
        with tempfile.TemporaryDirectory(prefix='log-profile-', dir=Path(output).parent) as work:
            start = time.perf_counter()
            if replay_rejects:
                # Reproduce the accepted input using this file's persisted
                # rejects, without repeating the expensive validation scan.
                rejects = list(LogParseReject.objects.filter(logfile=logfile).values(
                    'line_number', 'raw_line', 'error_code', 'error_message'))
                by_line = {row['line_number']: row for row in rejects}
                clean = Path(work) / 'validated.log'
                count = accepted = rejected = 0
                with source.open(encoding='utf-8', newline='') as raw, clean.open('w', encoding='utf-8', newline='') as dest:
                    for number, line in enumerate(raw, 1):
                        line = line.rstrip('\r\n')
                        if line.startswith('#'):
                            continue
                        count += 1
                        if number in by_line:
                            assert line.replace('\0', '\\0') == by_line[number]['raw_line'], 'Persisted reject differs from input'
                            rejected += 1
                            continue
                        assert '\0' not in line
                        dest.write(line + '\n')
                        accepted += 1
                assert rejected == len(rejects)
                validation = dict(validated_file=str(clean), source_count=count, parsed_count=accepted,
                                  rejected_count=rejected, rejects=rejects)
                timings['REPLAY_PREPARATION'] = time.perf_counter() - start
            else:
                validation = view.prepare_validated_logfile(str(source), logfile, work)
            view.analysis_progress.report('AFTER_VALIDATION')
            result['source_count'] = validation['source_count']
            result['valid_count'] = validation['parsed_count']
            result['reject_count'] = validation['rejected_count']
            if baseline:
                previous = json.loads(Path(baseline).read_text(encoding='utf-8'))
                assert previous['file_id'] == file_id
                assert previous['source_bytes'] == source.stat().st_size
                for key in ('source_count', 'valid_count', 'reject_count'):
                    assert result[key] == previous['rounds'][0][key], key
                previous_rejects = list(LogParseReject.objects.filter(logfile=logfile).values(
                    'line_number', 'raw_line', 'error_code', 'error_message'))
                assert validation['rejects'] == previous_rejects
                excluded = {item['line_number'] for item in previous_rejects}
                expected_hash = hashlib.sha256()
                with source.open(encoding='utf-8', newline='') as raw:
                    for number, line in enumerate(raw, 1):
                        line = line.rstrip('\r\n')
                        if number not in excluded and not line.startswith('#'):
                            expected_hash.update((line + '\n').encode('utf-8'))
                with open(validation['validated_file'], 'rb') as accepted:
                    actual_hash = hashlib.file_digest(accepted, 'sha256').hexdigest()
                assert actual_hash == expected_hash.hexdigest()
                result['baseline_validation_equivalent'] = True
                result['validated_sha256'] = actual_hash
                print('Accepted file bytes and rejected rows match the previous analysis.', flush=True)
            reject_table = 'profile_reject_' + uuid.uuid4().hex
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(f'CREATE TABLE {quote(reject_table)} (LIKE {quote(LogParseReject._meta.db_table)} INCLUDING ALL)')
                t = time.perf_counter()
                with connection.cursor() as cursor:
                    cursor.execute(f'DELETE FROM {quote(reject_table)} WHERE logfile_id = %s', [str(logfile.pk)])
                with patch.object(LogParseReject._meta, 'db_table', reject_table):
                    # Explicit surrogate IDs avoid advancing production sequences.
                    LogParseReject.objects.bulk_create([
                        LogParseReject(id=index + 1, logfile=logfile, **item)
                        for index, item in enumerate(validation['rejects'])
                    ])
                timings['REJECT_PERSISTENCE'] = time.perf_counter() - t
                transaction.set_rollback(True)
            read_csv, to_csv = pd.read_csv, pd.DataFrame.to_csv
            reads = []
            def measured_read(*args, **kwargs):
                t = time.perf_counter()
                value = read_csv(*args, **kwargs)
                reads.append(time.perf_counter() - t)
                return value
            def measured_write(*args, **kwargs):
                t = time.perf_counter()
                try:
                    return to_csv(*args, **kwargs)
                finally:
                    timings['CSV_WRITE'] += time.perf_counter() - t
            view.analysis_progress.report('PARSING')
            with patch.object(pd, 'read_csv', measured_read), patch.object(pd.DataFrame, 'to_csv', measured_write):
                csv_file = view.parse_apache_log(validation['validated_file'], str(logfile.pk), 0, None, None, 0, 0, work)
            view.analysis_progress.report('DB_SETUP')
            result['csv_bytes'] = Path(csv_file).stat().st_size
            result['pandas_read_seconds'] = reads
            timings['TRANSFORM_OTHER'] = timings['PARSING'] - sum(reads) - timings['CSV_WRITE']
            table = 'profile_log_' + uuid.uuid4().hex
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(f'CREATE TABLE {quote(table)} (LIKE {quote(model._meta.db_table)} INCLUDING ALL)')
                target = SimpleNamespace(_meta=SimpleNamespace(db_table=table, local_fields=model._meta.local_fields))
                view.analysis_progress.report('COPY')
                view.copy_csv_to_model(target, csv_file)
                view.analysis_progress.report('VERIFYING')
                with connection.cursor() as cursor:
                    cursor.execute(f'SELECT count(*) FROM {quote(table)} WHERE logfile_id = %s', [str(logfile.pk)])
                    result['stored_count'] = cursor.fetchone()[0]
                assert result['stored_count'] == result['valid_count']
                view.analysis_progress.report('ROLLBACK')
                transaction.set_rollback(True)
            view.analysis_progress.report('DONE')
            result['wall_seconds'] = time.perf_counter() - start
            result['seconds'] = dict(timings)
            result['pipeline_seconds'] = sum(timings[key] for key in ('READING', 'VALIDATING', 'PARSING', 'COPY', 'VERIFYING'))
        telemetry.close()
        report['rounds'].append(result)
        save()
        print(json.dumps(result), flush=True)

    # Profile a bounded, evenly spaced sample separately; cProfile overhead
    # must not contaminate the full-file wall-clock comparison above.
    index = view.get_logformat_index(logfile.file_format, logfile.format_kind)
    expected = max(index.values()) + 1
    stride = max(1, report['rounds'][0]['source_count'] // 2000)
    sample = []
    with source.open(encoding='utf-8') as handle:
        for number, line in enumerate(handle):
            if number % stride == 0 and not line.startswith('#'):
                sample.append(line.rstrip('\r\n'))
            if len(sample) >= 2000:
                break
    profiler = cProfile.Profile()
    profiler.enable()
    for line in sample:
        parsers.validate_log_line(line, logfile.format_kind, logfile.format_name, index, expected)
    profiler.disable()
    stats = pstats.Stats(profiler)
    selected = []
    for (filename, lineno, name), (cc, nc, tt, ct, callers) in stats.stats.items():
        if name in {'validate_log_line', 'split_log_fields', 'split', 'read_token', '_strptime_datetime', '_strptime', '<built-in method strptime>'} or 'strptime' in name:
            selected.append({'file': Path(filename).name, 'line': lineno, 'function': name, 'calls': nc, 'self_seconds': tt, 'cumulative_seconds': ct})
    report['validation_profile'] = {'sample_lines': len(sample), 'total_profiled_seconds': stats.total_tt, 'functions': sorted(selected, key=lambda row: -row['cumulative_seconds'])}
    save()
    print(json.dumps(report['validation_profile']), flush=True)


def validation_detail(output):
    """Low-overhead component timing, separate from cProfile measurements."""
    from loganalyzerapi import parsers
    from loganalyzerapi.views import DynamicLogDetailViewSet
    report = json.loads(Path(output).read_text(encoding='utf-8'))
    logfile = LogFile.objects.get(pk=report['file_id'])
    index = DynamicLogDetailViewSet().get_logformat_index(logfile.file_format, logfile.format_kind)
    expected = max(index.values()) + 1
    stride = max(1, report['rounds'][0]['source_count'] // 2000)
    sample = []
    with open(logfile.file_object.path, encoding='utf-8') as raw:
        for number, line in enumerate(raw):
            if number % stride == 0 and not line.startswith('#') and '\0' not in line:
                sample.append(line.rstrip('\r\n'))
            if len(sample) >= 2000:
                break
    original_split = parsers.shlex.split
    original_datetime = parsers.datetime
    results = []
    for repeat in range(3):
        times = defaultdict(float)
        def split(*args, **kwargs):
            start = time.perf_counter()
            try:
                return original_split(*args, **kwargs)
            finally:
                times['shlex_split'] += time.perf_counter() - start
        class MeasuredDateTime:
            @staticmethod
            def strptime(*args):
                start = time.perf_counter()
                try:
                    return original_datetime.strptime(*args)
                finally:
                    times['datetime_strptime'] += time.perf_counter() - start
        start = time.perf_counter()
        with patch.object(parsers.shlex, 'split', split), patch.object(parsers, 'datetime', MeasuredDateTime):
            for line in sample:
                assert parsers.validate_log_line(line, logfile.format_kind, logfile.format_name, index, expected) is None
        total = time.perf_counter() - start
        results.append({'total_seconds': total, **times, 'other_seconds': total - sum(times.values())})
    report['validation_component_timing'] = {'sample_lines': len(sample), 'runs': results}
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report['validation_component_timing']), flush=True)


def audit(output):
    from django.db import connection
    from dynamic_models.models import ModelSchema
    from loganalyzerapi.models import LogParseReject
    report = json.loads(Path(output).read_text(encoding='utf-8'))
    logfile = LogFile.objects.get(pk=report['file_id'])
    model = ModelSchema.objects.get(name='logdetail_' + str(logfile.project_id)).as_model()
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM pg_tables WHERE tablename LIKE 'profile_log_%' OR tablename LIKE 'profile_reject_%'")
        remaining = cursor.fetchone()[0]
    report['post_measurement_audit'] = {
        'remaining_measurement_tables': remaining,
        'original_stored_count': model.objects.filter(logfile_id=str(logfile.pk)).count(),
        'original_reject_count': LogParseReject.objects.filter(logfile=logfile).count(),
    }
    assert remaining == 0
    assert report['post_measurement_audit']['original_stored_count'] == report['rounds'][0]['stored_count']
    assert report['post_measurement_audit']['original_reject_count'] == report['rounds'][0]['reject_count']
    Path(output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report['post_measurement_audit']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-id')
    parser.add_argument('--output', default='scripts/log-pipeline-profile.json')
    parser.add_argument('--rounds', type=int, default=2)
    parser.add_argument('--replay-rejects', action='store_true')
    parser.add_argument('--detail-only', action='store_true')
    parser.add_argument('--audit-only', action='store_true')
    parser.add_argument('--baseline')
    args = parser.parse_args()
    if args.audit_only:
        audit(args.output)
    elif args.detail_only:
        validation_detail(args.output)
    elif args.file_id:
        benchmark(args.file_id, args.output, args.rounds, args.replay_rejects, args.baseline)
    else:
        inventory()
