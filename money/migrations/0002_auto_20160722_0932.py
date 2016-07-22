# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='user',
            field=models.ForeignKey(verbose_name='Денег на счету', to=settings.AUTH_USER_MODEL),
        ),
    ]
