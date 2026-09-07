from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loganalyzerapi', '0004_logparsereject'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAnalysisJob',
            fields=[
                ('job_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('PARTIAL', 'Partial'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('diff_hour', models.IntegerField(default=0)),
                ('source_count', models.PositiveIntegerField(default=0)),
                ('parsed_count', models.PositiveIntegerField(default=0)),
                ('rejected_count', models.PositiveIntegerField(default=0)),
                ('stored_count', models.PositiveIntegerField(default=0)),
                ('error_message', models.TextField(blank=True, default='')),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('logfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_jobs', to='loganalyzerapi.LogFile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_jobs', to='loganalyzerapi.LogMaster')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
