import json

from django.core.management.base import BaseCommand, CommandError

from loganalyzerapi.models import LogDetailV2, LogFile


class Command(BaseCommand):
    help = 'Report V2 storage readiness and dynamic/V2 row coverage.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--require-match', action='store_true',
            help='Exit with an error when any dynamic/V2 counts differ.',
        )

    def handle(self, *args, **options):
        from django.conf import settings
        from dynamic_models.models import ModelSchema

        report = {
            'storage_mode': settings.LOG_STORAGE_MODE,
            'logfiles': 0,
            'v2_rows': 0,
            'dynamic_rows': 0,
            'coverage': [],
        }
        for logfile in LogFile.objects.all().iterator():
            report['logfiles'] += 1
            v2_count = LogDetailV2.objects.filter(logfile=logfile).count()
            dynamic_count = 0
            try:
                schema = ModelSchema.objects.get(
                    name='logdetail_' + str(logfile.project_id)
                )
                dynamic_count = schema.as_model().objects.filter(
                    logfile_id=str(logfile.logfile_id)
                ).count()
            except ModelSchema.DoesNotExist:
                pass
            report['v2_rows'] += v2_count
            report['dynamic_rows'] += dynamic_count
            report['coverage'].append({
                'logfile_id': str(logfile.logfile_id),
                'dynamic_count': dynamic_count,
                'v2_count': v2_count,
                'matches': dynamic_count == v2_count,
            })
        report['ready_for_v2'] = all(item['matches'] for item in report['coverage'])
        self.stdout.write(json.dumps(report, ensure_ascii=False, indent=2))
        if options['require_match'] and not report['ready_for_v2']:
            raise CommandError('V2 readiness check failed: row counts differ')
