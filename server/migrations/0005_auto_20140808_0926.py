# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20140807_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='server',
            name='last_updated',
        ),
    ]
