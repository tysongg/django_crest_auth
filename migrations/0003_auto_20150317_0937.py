# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crest_auth', '0002_crest_user_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRESTUser',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('character_name', models.CharField(unique=True, max_length=250)),
                ('refresh_token', models.CharField(default=b'', max_length=250)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='crest_user',
        ),
    ]
