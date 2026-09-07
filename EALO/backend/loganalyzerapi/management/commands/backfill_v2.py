from django.core.management.base import BaseCommand

from dynamic_models.models import ModelSchema
from loganalyzerapi.models import LogFile
from loganalyzerapi.views import DynamicLogDetailViewSet


class Command(BaseCommand):
    help = 'Backfill LogDetailV2 from existing dynamic log-detail rows.'

    def handle(self, *args, **options):
        parser = DynamicLogDetailViewSet()
        total = 0
        for logfile in LogFile.objects.all().iterator():
            try:
                schema = ModelSchema.objects.get(
                    name='logdetail_' + str(logfile.project_id)
                )
            except ModelSchema.DoesNotExist:
                continue
            count = parser.mirror_dynamic_rows_to_v2(
                schema.as_model(), logfile.logfile_id
            )
            total += count
            self.stdout.write('%s: %s rows' % (logfile.logfile_id, count))
        self.stdout.write(self.style.SUCCESS('Backfilled %s V2 rows.' % total))
