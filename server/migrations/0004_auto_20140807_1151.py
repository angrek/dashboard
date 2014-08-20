# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20140807_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='oslevel',
            new_name='os_level',
        ),
    ]
