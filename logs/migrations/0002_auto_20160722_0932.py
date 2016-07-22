# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='log_type',
            field=models.IntegerField(verbose_name='Тип события', choices=[(1, 'Автоматическая проверка состояния счета'), (2, 'Отправка письма с состоянием счета'), (3, 'Авторизация пользователя на сайте'), (4, 'Регистрация пользователя'), (5, 'Пользователь вышел из системы'), (6, 'Принудительная проверка состояния счета')]),
        ),
    ]
