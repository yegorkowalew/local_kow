# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_type',
            field=models.IntegerField(default=1, choices=[(1, 'Новости провайдера'), (2, 'Новости разработчика')], verbose_name='Тип новости'),
            preserve_default=False,
        ),
    ]
