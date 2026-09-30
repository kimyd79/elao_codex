from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import DynamicLogDetailViewSet


class XViewDetailsTests(SimpleTestCase):
    def test_xview_limit_boundary_and_no_sampling(self):
        for count in (1_000_000, 1_000_001):
            with self.subTest(count=count):
                queryset = MagicMock()
                queryset.filter.return_value = queryset
                queryset.order_by.return_value = queryset
                queryset.count.return_value = count
                queryset.values.return_value.iterator.return_value = iter([
                    {'fdatetime': '20260922090000', 'ftime_taken': 1000, 'fstatus': 200, 'logfile_id': 'f1'},
                    {'fdatetime': '20260922090001', 'ftime_taken': 2000, 'fstatus': 500, 'logfile_id': 'f1'},
                ])
                request = APIRequestFactory().post('/mwla/logdetail_dynamic/xview/', {'project_id': 'p1', 'filter': {}, 'point_limit': 1}, format='json')
                force_authenticate(request, user=MagicMock(is_authenticated=True))
                with patch.object(DynamicLogDetailViewSet, 'get_queryset', return_value=queryset), patch('loganalyzerapi.views.LogFile.objects.filter'):
                    response = DynamicLogDetailViewSet.as_view({'post': 'xview'})(request)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data['limit_exceeded'], count > 1_000_000)
                if count > 1_000_000:
                    queryset.values.assert_not_called()
                    self.assertEqual(response.data['points'], [])
                else:
                    self.assertEqual(len(response.data['points']), 2)
                    queryset.values.return_value.iterator.assert_called_once()

    def test_selection_applies_original_filters_uri_time_and_duration(self):
        queryset = MagicMock()
        queryset.filter.return_value = queryset
        queryset.annotate.return_value = queryset
        queryset.order_by.return_value = queryset
        queryset.count.return_value = 42
        queryset.values.return_value.__getitem__.return_value = [{'id': 1}]
        request = APIRequestFactory().post('/mwla/logdetail_dynamic/xview_details/', {
            'project_id': 'p1', 'filter': {'xview_uri': '/a?b=1'},
            'bounds': {'start': '20260922090000', 'end': '20260922090100', 'lower': 10.5, 'upper': 20.5},
            'limit': 20, 'offset': 20, 'ordering': '-xview_ms',
        }, format='json')
        force_authenticate(request, user=MagicMock(is_authenticated=True))
        with patch.object(DynamicLogDetailViewSet, 'get_queryset', return_value=queryset) as base, patch('loganalyzerapi.views.LogFile.objects.filter', return_value=[]):
            response = DynamicLogDetailViewSet.as_view({'post': 'xview_details'})(request)
        self.assertEqual(response.status_code, 200)
        base.assert_called_once()
        queryset.filter.assert_any_call(fdatetime__range=('20260922090000', '20260922090100'), xview_ms__range=(10.5, 20.5))
        queryset.values.return_value.__getitem__.assert_called_once_with(slice(20, 40))
        queryset.order_by.assert_called_once_with('-xview_ms', 'id')
        self.assertEqual(response.data['count'], 42)

    def test_reversed_selection_is_rejected_before_query(self):
        request = APIRequestFactory().post('/mwla/logdetail_dynamic/xview_details/', {
            'bounds': {'start': '20260922090100', 'end': '20260922090000', 'lower': 10, 'upper': 20},
        }, format='json')
        force_authenticate(request, user=MagicMock(is_authenticated=True))
        with patch.object(DynamicLogDetailViewSet, 'get_queryset') as base:
            response = DynamicLogDetailViewSet.as_view({'post': 'xview_details'})(request)
        self.assertEqual(response.status_code, 400)
        base.assert_not_called()
