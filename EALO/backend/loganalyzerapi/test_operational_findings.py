from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIRequestFactory, force_authenticate

from .ai_dataset import authorize, prepare_queryset, validate_filter
from .models import LogDetail, LogFile, LogMaster
from .operational_findings import analyze, changes, measured_format, traffic_spikes
from .views import DynamicLogDetailViewSet


class FindingRulesTests(SimpleTestCase):
    databases = {'default'}

    def test_traffic_spike_uses_three_buckets_three_times_median_and_one_hundred_minimum(self):
        points = [dict(start=str(i), end=str(i+1), requests=n, partial=False)
                  for i, n in enumerate([34, 34, 34, 102])]
        self.assertEqual(traffic_spikes(points)[0]['baseline'], 34)
        self.assertEqual(traffic_spikes(points)[0]['observed'], 102)
        self.assertEqual(traffic_spikes(points[:3]), [])
        below_minimum = [dict(start=str(i), end=str(i+1), requests=n, partial=False)
                         for i, n in enumerate([20, 20, 20, 99])]
        self.assertEqual(traffic_spikes(below_minimum), [])

    def test_baseline_includes_zero_and_ignores_partial_bucket(self):
        points = [dict(start=str(i), end=str(i+1), requests=n, server_errors=e, partial=False)
                  for i, (n, e) in enumerate([(20, 0), (20, 0), (20, 0), (60, 10), (0, 0)])]
        self.assertEqual(changes(points, 'requests')[0]['baseline'], 20)
        self.assertEqual(len(changes(points, 'server_errors', True)), 1)
        points[3]['partial'] = True
        self.assertEqual(changes(points, 'requests'), [])
        self.assertEqual(changes(points, 'server_errors', True), [])

    def test_short_history_and_small_counts_do_not_trigger(self):
        points = [dict(start='a', end='b', requests=19, partial=False)] * 4
        self.assertEqual(changes(points, 'requests'), [])
        self.assertEqual(changes(points[:2], 'requests'), [])

    def test_estimated_formats_and_project_access(self):
        for fmt in ['%h %r %s', '$remote_addr $request', '']:
            self.assertFalse(measured_format(SimpleNamespace(file_format=fmt)))
        self.assertTrue(measured_format(SimpleNamespace(file_format='%h %r %D')))
        with self.assertRaises(PermissionDenied):
            authorize(SimpleNamespace(is_authenticated=True, is_staff=False, is_superuser=False, username='other'),
                      SimpleNamespace(creator='owner'))

    def test_api_rejects_invalid_input_before_queries(self):
        request = APIRequestFactory().post('/', {'project_id': 'invalid'}, format='json')
        force_authenticate(request, user=SimpleNamespace(is_authenticated=True))
        response = DynamicLogDetailViewSet.as_view({'post': 'operational_findings'})(request)
        self.assertEqual(response.status_code, 400)

    @patch('loganalyzerapi.views.logger.exception')
    @patch('loganalyzerapi.operational_findings.build_findings', side_effect=RuntimeError('query failed'))
    def test_api_logs_failure_with_traceback(self, _build, log_exception):
        request = APIRequestFactory().post('/', {
            'project_id': '00000000-0000-0000-0000-000000000001',
            'filter': {'searchValue': 'secret-value'},
        }, format='json')
        force_authenticate(request, user=SimpleNamespace(is_authenticated=True))
        with self.assertRaisesRegex(RuntimeError, 'query failed'):
            DynamicLogDetailViewSet.as_view({'post': 'operational_findings'})(request)
        log_exception.assert_called_once()
        self.assertNotIn('secret-value', str(log_exception.call_args))


class FindingsDatabaseTests(TestCase):
    def setUp(self):
        self.project = LogMaster.objects.create(project_name='finding-test', creator='owner')
        self.files = [LogFile.objects.create(project=self.project, file_format=fmt, server_name='server', instance_name='app')
                      for fmt in ['%h %r %s %D', '%h %r %s %T', '%h %r %s']]
        self.data = dict(dateFromValue='20260101', timeFromValue='000000', dateToValue='20260101',
                         timeToValue='000559', projectServers=['server-app'])

    def result(self, **overrides):
        filters = validate_filter(self.project.pk, dict(self.data, **overrides))
        query = prepare_queryset(LogDetail.objects.all(), self.files, filters)
        return analyze(query, self.files, filters['start'], filters['end'])

    def test_mixed_units_percentiles_errors_404_and_estimates(self):
        rows = []
        for minute, count in enumerate([33, 33, 33, 100, 33, 33]):
            for n in range(count):
                file = self.files[n % 2]
                rows.append(LogDetail(logfile=file, fdatetime=f'20260101000{minute}00',
                    fip='192.0.2.1', frequest='GET /api HTTP/1.1', freferer='https://example.test/',
                    fstatus=('500' if n < 10 else '404' if n < 20 else '200') if minute == 3 else '200',
                    ftime_taken=(2_000_000 if n % 2 == 0 else 2)))
        rows.append(LogDetail(logfile=self.files[2], fdatetime='20260101000500', fstatus='200',
                              frequest='GET /estimated', ftime_taken=999_000_000))
        LogDetail.objects.bulk_create(rows)
        result = self.result()
        traffic, performance, errors, missing = result['findings']
        self.assertEqual(result['total'], 266)
        self.assertEqual(traffic['evidence']['spike_count'], 1)
        self.assertNotIn('top_ips', traffic['evidence'])
        self.assertNotIn('top_requests', traffic['evidence'])
        self.assertEqual(performance['evidence']['count'], 265)
        self.assertEqual(performance['evidence']['excluded'], 1)
        self.assertEqual(performance['evidence']['p95_ms'], 2000)
        self.assertEqual(performance['evidence']['p99_ms'], 2000)
        self.assertEqual(errors['evidence']['count'], 10)
        self.assertEqual(errors['evidence']['increase_count'], 1)
        self.assertEqual(missing['evidence']['count'], 10)
        self.assertEqual(missing['evidence']['referrers'][0]['freferer'], 'https://example.test/')
        filtered = self.result(conditionValue='S', searchValue='404')
        self.assertEqual(filtered['total'], 10)
        self.assertEqual(filtered['findings'][2]['evidence']['count'], 0)
        self.assertEqual(self.result(projectServers=[])['total'], 0)

    def test_empty_scope_and_missing_measured_times(self):
        self.assertTrue(all(row['status'] == 'insufficient' for row in self.result()['findings']))
        LogDetail.objects.create(logfile=self.files[2], fdatetime='20260101000000', fstatus='200', ftime_taken=9000000)
        result = self.result()
        self.assertEqual(result['findings'][1]['status'], 'insufficient')
        self.assertIsNone(result['findings'][1]['evidence']['p95_ms'])
        self.assertEqual(result['findings'][2]['status'], 'clear')

    def test_findings_always_use_sixty_second_buckets(self):
        result = self.result(timeToValue='020000')
        self.assertEqual(result['scope']['bucket_seconds'], 60)

    def test_api_authorization_and_one_sided_filter(self):
        from django.urls import resolve
        route = resolve('/mwla/logdetail_dynamic/operational_findings/').func
        factory = APIRequestFactory()
        payload = dict(project_id=str(self.project.pk), filter={'ttFromValue': '2000'})
        anonymous = route(factory.post('/', payload, format='json'))
        self.assertEqual(anonymous.status_code, 401)
        stranger = factory.post('/', payload, format='json')
        force_authenticate(stranger, user=SimpleNamespace(is_authenticated=True, username='other',
                                                         is_staff=False, is_superuser=False))
        self.assertEqual(route(stranger).status_code, 403)
        for duration in (2, 3):
            LogDetail.objects.create(logfile=self.files[1], fdatetime='20260101000000',
                                     fstatus='200', ftime_taken=duration)
        request = factory.post('/', payload, format='json')
        force_authenticate(request, user=SimpleNamespace(is_authenticated=True, username='owner',
                                                        is_staff=False, is_superuser=False))
        with patch('loganalyzerapi.operational_findings.get_object_or_404',
                   side_effect=[self.project, SimpleNamespace(as_model=lambda: LogDetail)]):
            response = route(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total'], 1)
        self.assertEqual(response.data['findings'][1]['evidence']['p95_ms'], 3000)
