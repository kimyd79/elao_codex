"""Offline SQLite ORM tests; set PYTHONPATH to EALO/backend and execute directly.

Kept outside Django test discovery to avoid loading standalone settings there.
"""
import unittest
from types import SimpleNamespace
from uuid import UUID

from django.conf import settings

if not settings.configured:
    settings.configure(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
                       INSTALLED_APPS=[], SECRET_KEY='offline-test')
    import django
    django.setup()

from django.db import connection, models
from django.test.utils import CaptureQueriesContext
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from loganalyzerapi.ai_dataset import validate_filter, authorize, prepare_queryset, build_dataset, metrics, detect_candidates


class Row(models.Model):
    logfile_id = models.UUIDField()
    fdatetime = models.CharField(max_length=14, db_index=True)
    fip = models.CharField(max_length=40, null=True)
    frequest = models.TextField()
    freferer = models.TextField(default='')
    fuser_agent = models.TextField(default='')
    fstatus = models.CharField(max_length=10)
    ftime_taken = models.FloatField(null=True)
    log_line = models.TextField(default='')

    class Meta:
        app_label = 'ai_offline'


PID = '00000000-0000-0000-0000-000000000001'
FID = UUID('00000000-0000-0000-0000-000000000002')
SECOND_FID = UUID('00000000-0000-0000-0000-000000000003')


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with connection.schema_editor() as editor:
            editor.create_model(Row)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as editor:
            editor.delete_model(Row)

    def setUp(self):
        Row.objects.all().delete()
        self.data = dict(dateFromValue='20260916', timeFromValue='120000',
                         dateToValue='20260916', timeToValue='120009',
                         projectServers=['web-1-app-1'], excludeSearch='false')
        self.files = [SimpleNamespace(logfile_id=FID, server_name='web-1', instance_name='app-1', file_format='%D'),
                      SimpleNamespace(logfile_id=SECOND_FID, server_name='web-1', instance_name='app-1', file_format='%T')]

    def query(self, **changes):
        filters = validate_filter(PID, {**self.data, **changes})
        return prepare_queryset(Row.objects.all(), self.files, filters), filters

    def add(self, second=0, count=1, **kwargs):
        defaults = dict(logfile_id=FID, fdatetime=f'202609161200{second:02}',
                        fip='192.0.2.1', frequest='GET /api/search HTTP/1.1',
                        fstatus='200', ftime_taken=1000, log_line='sample')
        Row.objects.bulk_create([Row(**{**defaults, **kwargs}) for _ in range(count)])

    def test_mixed_units_and_zero_bound(self):
        self.add(ftime_taken=1000)
        self.add(logfile_id=SECOND_FID, ftime_taken=.001)
        self.add(ftime_taken=0)
        self.assertEqual(metrics(self.query(ttFromValue=1, ttToValue=1)[0])['requests'], 2)
        self.assertEqual(metrics(self.query(ttFromValue=0, ttToValue=0)[0])['requests'], 1)

    def test_false_exclude_and_empty_instances(self):
        self.add(fstatus='500')
        self.add(fstatus='200')
        self.assertEqual(metrics(self.query(conditionValue='S', searchValue='500')[0])['requests'], 1)
        self.assertEqual(metrics(self.query(conditionValue='S', searchValue='500', excludeSearch=True)[0])['requests'], 1)
        self.assertEqual(metrics(self.query(projectServers=[])[0])['requests'], 0)

    def test_time_bounds(self):
        self.add(second=0)
        self.add(second=9)
        self.add(second=10)
        self.assertEqual(metrics(self.query()[0])['requests'], 2)

    def test_invalid_filters(self):
        for changes in [dict(project_id='different'), dict(timeToValue='999999'),
                        dict(ttFromValue='nan'), dict(ttFromValue=2, ttToValue=1),
                        dict(projectServers='web'), dict(conditionValue='sql')]:
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                self.query(**changes)

    def test_authorization(self):
        with self.assertRaises(NotAuthenticated):
            authorize(None, SimpleNamespace(creator='owner'))
        user = SimpleNamespace(is_authenticated=True, is_staff=False, is_superuser=False, username='other')
        with self.assertRaises(PermissionDenied):
            authorize(user, SimpleNamespace(creator='owner'))
        user.username = 'owner'
        authorize(user, SimpleNamespace(creator='owner'))

    def test_spike_evidence_and_bounded_samples(self):
        for second in range(10):
            self.add(second=second, count=100 if second == 4 else 20,
                     fstatus='500' if second == 4 else '200', ftime_taken=400000 if second == 4 else 1000)
        with CaptureQueriesContext(connection) as captured:
            result = build_dataset(*self.query())
        self.assertEqual(result['summary']['requests'], 280)
        self.assertEqual(sum(p['requests'] for p in result['timeline']), 280)
        self.assertIn('b4', [c['bucket_id'] for c in result['candidates']])
        detail = next(d for d in result['details'] if d['bucket_id'] == 'b4')
        self.assertEqual(detail['entities']['ips'][0]['previous_count'], 20)
        self.assertEqual(detail['entities']['ips'][0]['current_count'], 100)
        self.assertLessEqual(len(result['samples']), 200)
        self.assertEqual(len({s['id'] for s in result['samples']}), len(result['samples']))
        self.assertLess(len(captured), 200)

    def test_empty_has_zero_buckets_not_incidents(self):
        result = build_dataset(*self.query())
        self.assertEqual(result['summary']['requests'], 0)
        self.assertEqual(result['candidates'], [])
        self.assertEqual(result['samples'], [])

    def test_large_input_byte_budget(self):
        self.add(count=250, log_line='가' * 3000)
        import json
        result = build_dataset(*self.query())
        self.assertLessEqual(len(json.dumps(result, ensure_ascii=False).encode()), 128*1024)

    def test_drop_and_partial(self):
        points = [dict(id=f'b{i}', requests=100 if i < 3 else 0, unique_ips=40 if i < 3 else 0,
                       errors=0, avg_ms=None, partial=False) for i in range(4)]
        self.assertEqual(len(detect_candidates(points)), 1)
        points[-1]['partial'] = True
        self.assertEqual(detect_candidates(points), [])

    def test_constant_total_entity_replacement(self):
        for second in range(10):
            self.add(second=second, count=30, fip='old' if second < 4 else 'new',
                     frequest='/old' if second < 4 else '/new')
        result = build_dataset(*self.query())
        self.assertEqual({p['requests'] for p in result['timeline']}, {30})
        changes = [c for c in result['entity_changes'] if c['bucket_id'] == 'b4']
        self.assertEqual({(c['field'], c['direction']) for c in changes},
                         {('fip', 'increase'), ('fip', 'decrease'), ('frequest', 'increase'), ('frequest', 'decrease')})
        self.assertTrue(any(d['bucket_id'] == 'b4' for d in result['details']))

    def test_stable_entities_no_false_positive(self):
        for second in range(10):
            self.add(second=second, count=30)
        self.assertEqual(build_dataset(*self.query())['entity_changes'], [])

    def test_top_rank_dropout_is_not_zero(self):
        for second in range(10):
            for entity in range(11):
                self.add(second=second, count=29 if second == 4 and entity == 0 else 30,
                         fip=f'ip-{entity:02}', frequest=f'/url-{entity:02}')
        result = build_dataset(*self.query())
        self.assertFalse(any(c['value'] in ('ip-00', '/url-00') for c in result['entity_changes']))

    def test_100000_rows_bounded_aggregation(self):
        import time
        for second in range(10):
            self.add(second=second, count=10000)
        started = time.monotonic()
        with CaptureQueriesContext(connection) as captured:
            result = build_dataset(*self.query())
        self.assertEqual(result['summary']['requests'], 100000)
        self.assertLessEqual(len(result['samples']), 200)
        self.assertLessEqual(len(result['timeline']), 120)
        self.assertLess(len(captured), 30)
        print(f'\nOffline 100k: {time.monotonic()-started:.3f}s, {len(captured)} queries, '
              f'{len(result["samples"])} samples')


if __name__ == '__main__':
    unittest.main()
