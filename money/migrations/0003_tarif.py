# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_auto_20160703_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('money_for_mons', models.PositiveIntegerField(default=False)),
            ],
        ),
    ]
