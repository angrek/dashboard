# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='xcelys',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='last_updated',
            field=models.DateTimeField(null=True, verbose_name='last updated', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='ssl',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='exception',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='os',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='log',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='active',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='java',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='centrify',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='server',
            name='oslevel',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
