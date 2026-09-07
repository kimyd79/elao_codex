from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loganalyzerapi', '0003_expand_dynamic_model_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogParseReject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_number', models.PositiveIntegerField()),
                ('raw_line', models.TextField()),
                ('error_code', models.CharField(max_length=50)),
                ('error_message', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('logfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parse_rejects', to='loganalyzerapi.LogFile')),
            ],
            options={
                'ordering': ['line_number'],
            },
        ),
    ]
