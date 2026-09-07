from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loganalyzerapi', '0005_loganalysisjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='logfile',
            name='content_sha256',
            field=models.CharField(blank=True, db_index=True, max_length=64, null=True),
        ),
    ]
