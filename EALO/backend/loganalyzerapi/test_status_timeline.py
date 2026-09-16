from unittest.mock import MagicMock

from django.test import SimpleTestCase

from loganalyzerapi.chart_aggregation import status_timeline


class StatusTimelineTests(SimpleTestCase):
    def aggregate(self, rows, timeline):
        query = MagicMock()
        query.order_by.return_value = query
        query.annotate.return_value = query
        query.values.return_value = query
        query.iterator.return_value = iter(rows)
        result = status_timeline(query, timeline)
        query.iterator.assert_called_once_with(chunk_size=4096)
        return result

    def test_status_groups_and_other_status_only_buckets(self):
        for timeline, bucket in [('1', '2026010100'), ('2', '202601010001'), ('3', '20260101000102')]:
            with self.subTest(timeline=timeline):
                result = self.aggregate([
                    {'f_date': bucket, 'f_status': '2', 'status_count': 12},
                    {'f_date': bucket, 'f_status': '5', 'status_count': 3},
                    {'f_date': bucket + '9', 'f_status': '1', 'status_count': 7},
                ], timeline)
                self.assertEqual(result, ([bucket, bucket + '9'], [12, 0], [0, 0], [0, 0], [3, 0]))

    def test_empty_result(self):
        self.assertEqual(self.aggregate([], '3'), ([], [], [], [], []))
