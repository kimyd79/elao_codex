"""Best-effort, throttled telemetry; never changes parser or COPY semantics."""
import logging
import time

from django.db import connection

logger = logging.getLogger(__name__)


class AnalysisProgress:
    def __init__(self, job_id):
        self.job_id = str(job_id)
        self.db = None
        self.phase = None
        self.last_write = 0

    def report(self, phase, processed=0, total=0, unit='', force=False):
        if connection.in_atomic_block:
            # Uncommitted job rows cannot be observed from another connection.
            return
        now = time.monotonic()
        if not force and phase == self.phase and now - self.last_write < 1:
            return
        self.phase, self.last_write = phase, now
        try:
            # COPY occupies the main connection. Telemetry must use its own
            # autocommit connection and must not affect the data transaction.
            if self.db is None:
                self.db = connection.copy(alias='analysis_progress')
                with self.db.cursor() as cursor:
                    cursor.execute("SET statement_timeout = '1000ms'")
            with self.db.cursor() as cursor:
                cursor.execute(
                    'UPDATE loganalyzerapi_loganalysisjob SET phase=%s, '
                    'processed_units=%s, total_units=%s, progress_unit=%s, '
                    'updated=CURRENT_TIMESTAMP WHERE job_id=%s',
                    [phase, processed, total, unit, self.job_id],
                )
        except Exception:
            logger.warning('Could not update analysis progress', exc_info=True)
            self.close()

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None


class CopyProgressReader:
    def __init__(self, source, report, total):
        self.source, self.report, self.total = source, report, total
        self.processed = 0

    def read(self, size=-1):
        data = self.source.read(size)
        self.processed += len(data.encode('utf-8'))
        self.report('COPY', self.processed, self.total, 'bytes')
        return data
