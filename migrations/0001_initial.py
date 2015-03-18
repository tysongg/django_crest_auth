# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='crest_user',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('character_name', models.CharField(unique=True, max_length=250)),
                ('refresh_token', models.CharField(max_length=250, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
