import json
import tempfile
import time
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.test.utils import override_settings

from dynamic_models.models import ModelSchema
from loganalyzerapi.models import LogFile, LogMaster
from loganalyzerapi.views import DynamicLogDetailViewSet


class Command(BaseCommand):
    help = 'Benchmark AS-IS dynamic storage against TO-BE dual storage.'

    def add_arguments(self, parser):
        parser.add_argument('--repeats', type=int, default=2000)

    def handle(self, *args, **options):
        repeats = options['repeats']
        fixture = Path(__file__).resolve().parents[2] / 'testdata' / 'access_logs' / 'apache_combined.log'
        source = fixture.read_text(encoding='utf-8')
        sample_bytes = (source * repeats).encode('utf-8')
        parser = DynamicLogDetailViewSet()
        results = []

        with tempfile.TemporaryDirectory(prefix='elao-benchmark-') as temp_dir:
            for mode in ('dynamic', 'dual'):
                project = LogMaster.objects.create(
                    project_name='benchmark-' + mode,
                    project_description='temporary benchmark',
                    creator='benchmark',
                )
                project_id = str(project.project_id)
                schema = ModelSchema.objects.create(name='logdetail_' + project_id)
                fields = [
                    ('logfile_id', 'character', 64), ('log_line', 'character', 1000),
                    ('fyear', 'character', 4), ('fmonth', 'character', 2), ('fday', 'character', 2),
                    ('fhour', 'character', 2), ('fminute', 'character', 2), ('fsecond', 'character', 2),
                    ('fdate', 'character', 8), ('ftime', 'character', 6), ('fdatetime', 'character', 14),
                    ('frequest', 'character', 500), ('fip', 'character', 40), ('freferer', 'character', 500),
                    ('fuser_agent', 'character', 500), ('fstatus', 'character', 10),
                    ('ftime_taken', 'float', None), ('fbyte', 'integer', None), ('fextension', 'character', 10),
                    ('freserve1', 'character', 200), ('freserve2', 'character', 200), ('freserve3', 'character', 200),
                    ('created', 'date', None),
                ]
                from dynamic_models.models import FieldSchema
                for name, data_type, max_length in fields:
                    FieldSchema.objects.create(model_schema=schema, name=name, data_type=data_type, max_length=max_length, null=True)
                model = schema.as_model()
                path = Path(temp_dir) / (mode + '.log')
                path.write_bytes(sample_bytes)
                logfile = LogFile.objects.create(
                    project=project, file_name=path.name, file_object=ContentFile(sample_bytes, name=path.name),
                    file_format='%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i" %D',
                    format_kind='apache', format_name='combined', file_size=len(sample_bytes),
                    server_name='benchmark', instance_name='single',
                )
                csv_path = parser.parse_apache_log(str(path), str(logfile.logfile_id), 0, None, None, 0, 0, temp_dir)
                started = time.perf_counter()
                parser.copy_csv_to_model(model, csv_path)
                dynamic_load_seconds = time.perf_counter() - started
                dynamic_count = model.objects.filter(logfile_id=str(logfile.logfile_id)).count()
                v2_count = 0
                v2_load_seconds = 0
                if mode == 'dual':
                    v2_started = time.perf_counter()
                    v2_count = parser.mirror_dynamic_rows_to_v2(model, logfile.logfile_id)
                    v2_load_seconds = time.perf_counter() - v2_started
                elapsed = dynamic_load_seconds + v2_load_seconds
                results.append({
                    'mode': mode, 'bytes': len(sample_bytes), 'rows': dynamic_count,
                    'v2_rows': v2_count, 'elapsed_seconds': round(elapsed, 3),
                    'dynamic_copy_seconds': round(dynamic_load_seconds, 3),
                    'v2_mirror_seconds': round(v2_load_seconds, 3),
                    'rows_per_second': round(dynamic_count / elapsed, 1) if elapsed else 0,
                })
                schema.delete()
                project.delete()

        self.stdout.write(json.dumps({'repeats': repeats, 'fixture_rows': 5, 'results': results}, indent=2))
