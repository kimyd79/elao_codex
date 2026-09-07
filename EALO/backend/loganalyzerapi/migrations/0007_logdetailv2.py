import uuid

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loganalyzerapi', '0006_logfile_content_sha256'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDetailV2',
            fields=[
                ('log_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('event_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.SmallIntegerField(blank=True, null=True)),
                ('response_time', models.BigIntegerField(blank=True, null=True)),
                ('response_bytes', models.BigIntegerField(blank=True, null=True)),
                ('request', models.TextField(blank=True, null=True)),
                ('client_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('raw_line', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typed_details', to='loganalyzerapi.logfile')),
            ],
            options={
                'indexes': [
                    models.Index(fields=['logfile', 'event_at'], name='loganalyzer_logfile_e17ba2_idx'),
                    models.Index(fields=['logfile', 'status'], name='loganalyzer_logfile_93ac75_idx'),
                    models.Index(fields=['request'], name='loganalyzer_request_5167d4_idx'),
                ],
            },
        ),
    ]
