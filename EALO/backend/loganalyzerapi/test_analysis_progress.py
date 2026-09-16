import io
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from loganalyzerapi.analysis_progress import AnalysisProgress, CopyProgressReader


class AnalysisProgressTests(SimpleTestCase):
    def test_copy_reader_preserves_content_and_counts_utf8_bytes(self):
        report = MagicMock()
        reader = CopyProgressReader(io.StringIO('hello,한글\n'), report, 13)
        self.assertEqual(reader.read(6) + reader.read(), 'hello,한글\n')
        self.assertEqual(reader.processed, 13)
        report.assert_called_with('COPY', 13, 13, 'bytes')

    @patch('loganalyzerapi.analysis_progress.connection')
    @patch('loganalyzerapi.analysis_progress.time.monotonic')
    def test_updates_throttled_except_phase_changes(self, clock, connection):
        connection.in_atomic_block = False
        clock.side_effect = [10, 10.2, 11.1, 11.2]
        reporter = AnalysisProgress('example')
        reporter.report('VALIDATING', 1, 10, 'bytes')
        reporter.report('VALIDATING', 2, 10, 'bytes')
        reporter.report('VALIDATING', 3, 10, 'bytes')
        reporter.report('COPY', 0, 20, 'bytes')
        execute = connection.copy.return_value.cursor.return_value.__enter__.return_value.execute
        self.assertEqual(execute.call_count, 4)  # timeout setup + 3 updates
        reporter.close()
        connection.copy.return_value.close.assert_called_once()

    @patch('loganalyzerapi.analysis_progress.connection')
    def test_uncommitted_jobs_do_not_block_on_telemetry(self, connection):
        connection.in_atomic_block = True
        AnalysisProgress('example').report('READING')
        connection.copy.assert_not_called()
