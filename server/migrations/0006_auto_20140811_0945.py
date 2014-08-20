# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20140808_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='centrify',
            field=models.CharField(max_length=35, null=True, blank=True),
        ),
    ]
