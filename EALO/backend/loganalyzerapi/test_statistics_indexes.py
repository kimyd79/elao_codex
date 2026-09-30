from unittest.mock import patch

from django.test import SimpleTestCase

from .statistics_indexes import STATISTICS_INDEXES, statistics_index_statements


class StatisticsIndexTests(SimpleTestCase):
    @patch('loganalyzerapi.statistics_indexes.connection.vendor', 'postgresql')
    def test_concurrent_index_sql_covers_compact_statistics_columns(self):
        statements = statistics_index_statements(
            'loganalyzerapi_logdetail_00000000_0000_0000_0000_000000000000',
            concurrently=True,
        )
        self.assertEqual(len(statements), len(STATISTICS_INDEXES))
        self.assertTrue(all('CREATE INDEX CONCURRENTLY IF NOT EXISTS' in sql for sql in statements))
        combined = ' '.join(statements)
        self.assertIn('"fdatetime"', combined)
        self.assertIn('"fstatus"', combined)
        self.assertIn('"ftime_taken" DESC', combined)
        self.assertNotIn('"frequest"', combined)
        self.assertNotIn('"fuser_agent"', combined)
