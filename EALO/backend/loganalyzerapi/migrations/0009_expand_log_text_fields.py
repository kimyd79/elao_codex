from django.db import migrations, models


TEXT_FIELDS = ('log_line', 'frequest', 'freferer', 'fuser_agent')


def expand_dynamic_log_fields(apps, schema_editor):
    """Keep existing per-project dynamic tables aligned with LogDetail."""
    ModelSchema = apps.get_model('dynamic_models', 'ModelSchema')
    FieldSchema = apps.get_model('dynamic_models', 'FieldSchema')
    existing_tables = set(schema_editor.connection.introspection.table_names())
    quote = schema_editor.quote_name

    for model_schema in ModelSchema.objects.filter(name__startswith='logdetail_').iterator():
        table_name = 'loganalyzerapi_' + model_schema.name.replace('-', '_')
        if table_name in existing_tables:
            for field_name in TEXT_FIELDS:
                schema_editor.execute(
                    f'ALTER TABLE {quote(table_name)} '
                    f'ALTER COLUMN {quote(field_name)} TYPE text'
                )
        FieldSchema.objects.filter(
            model_schema_id=model_schema.pk,
            name__in=TEXT_FIELDS,
        ).update(data_type='text', max_length=None)


class Migration(migrations.Migration):
    dependencies = [('loganalyzerapi', '0008_analysis_progress')]

    operations = [
        migrations.AlterField(
            model_name='logdetail',
            name='freferer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logdetail',
            name='frequest',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logdetail',
            name='fuser_agent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='logdetail',
            name='log_line',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(expand_dynamic_log_fields, migrations.RunPython.noop),
    ]
