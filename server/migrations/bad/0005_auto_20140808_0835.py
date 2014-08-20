# encoding: utf8
from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20140807_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='created',
            field=models.DateTimeField(default=datetime(2014, 8, 8, 8, 34, 46, 886529), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='server',
            name='modified',
            field=models.DateTimeField(default=datetime(2014, 8, 8, 8, 35, 8, 902490)),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='server',
            name='last_updated',
        ),
    ]
