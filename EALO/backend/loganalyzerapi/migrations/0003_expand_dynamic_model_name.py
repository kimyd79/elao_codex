from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('loganalyzerapi', '0002_auto_20260811_1614'),
        ('dynamic_models', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                'ALTER TABLE dynamic_models_modelschema '
                'ALTER COLUMN name TYPE varchar(64)'
            ),
            reverse_sql=(
                'ALTER TABLE dynamic_models_modelschema '
                'ALTER COLUMN name TYPE varchar(32)'
            ),
        ),
    ]
