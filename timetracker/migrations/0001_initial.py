# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('short_name', models.CharField(max_length=5, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                u'verbose_name': 'Category',
                u'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
    ]
