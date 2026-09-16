from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('loganalyzerapi', '0007_logdetailv2')]
    operations = [
        migrations.AddField('loganalysisjob', 'run_id', models.UUIDField(null=True, blank=True, db_index=True)),
        migrations.AddField('loganalysisjob', 'phase', models.CharField(max_length=32, blank=True, default='')),
        migrations.AddField('loganalysisjob', 'processed_units', models.PositiveBigIntegerField(default=0)),
        migrations.AddField('loganalysisjob', 'total_units', models.PositiveBigIntegerField(default=0)),
        migrations.AddField('loganalysisjob', 'progress_unit', models.CharField(max_length=16, blank=True, default='')),
    ]
