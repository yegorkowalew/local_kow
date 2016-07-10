# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('log_type', models.IntegerField(verbose_name='Тип события', choices=[(1, 'Автоматическая проверка состояния счета'), (2, 'Отправка письма с состоянием счета'), (3, 'Авторизация пользователя на сайте'), (4, 'Регистрация пользователя')])),
                ('log_status', models.CharField(verbose_name='Статус', max_length=10)),
                ('log_date', models.DateTimeField(verbose_name='Дата создания', default=django.utils.timezone.now)),
                ('log_user', models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Лог',
            },
        ),
    ]
