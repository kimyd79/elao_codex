import uuid

from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from dynamic_models.models import ModelSchema

from loganalyzerapi.statistics_indexes import ensure_statistics_indexes


class Command(BaseCommand):
    help = 'Create compact indexes used by statistics queries on dynamic log tables.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--project-id',
            help='Optimize one project. Omit only when using --all.',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Optimize every existing dynamic log table.',
        )
        parser.add_argument(
            '--concurrently',
            action='store_true',
            help='Build PostgreSQL indexes without blocking reads and writes.',
        )

    def handle(self, *args, **options):
        project_id = options['project_id']
        if bool(project_id) == bool(options['all']):
            raise CommandError('Specify exactly one of --project-id or --all.')
        if options['concurrently'] and connection.in_atomic_block:
            raise CommandError('Concurrent index creation cannot run in a transaction.')

        if project_id:
            try:
                project_id = str(uuid.UUID(project_id))
            except (TypeError, ValueError):
                raise CommandError('project-id must be a valid UUID')
            schemas = ModelSchema.objects.filter(name='logdetail_' + project_id)
        else:
            schemas = ModelSchema.objects.filter(name__startswith='logdetail_').order_by('name')

        if not schemas.exists():
            raise CommandError('No matching dynamic log table was found.')
        for schema in schemas.iterator():
            ensure_statistics_indexes(schema.as_model(), options['concurrently'])
            self.stdout.write(self.style.SUCCESS('Optimized %s' % schema.db_table))
