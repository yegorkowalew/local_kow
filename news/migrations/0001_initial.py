# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Название новости', max_length=200)),
                ('text', models.TextField(verbose_name='Содержание новости')),
                ('created_date', models.DateTimeField(verbose_name='Дата создания', default=django.utils.timezone.now)),
                ('parsed_date', models.DateTimeField(blank=True, verbose_name='Дата парсера', null=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
    ]
