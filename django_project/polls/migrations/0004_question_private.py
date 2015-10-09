# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_question_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
