# encoding: utf8
from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('username', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, to_field=u'id')),
                ('modified', models.DateTimeField(auto_now_add=True, null=True)),
                ('description', models.CharField(max_length=40, null=True, blank=True)),
                ('category', models.ForeignKey(to='timetracker.Category', to_field='name')),
                ('hours', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
