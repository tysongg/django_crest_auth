# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crest_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crest_user',
            name='last_login',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
