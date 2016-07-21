# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from local_site.settings import TYPE_CHOICES

"""TYPE_CHOICES = (
    (1, 'Автоматическая проверка состояния счета'),
    (2, 'Отправка письма с состоянием счета'),
    (3, 'Авторизация пользователя на сайте'),
    (4, 'Регистрация пользователя'),
    (5, 'Пользователь разлогинился'),
    (6, 'Принудительная проверка состояния счета'),
)"""

class Logs(models.Model):
    log_user = models.ForeignKey(
                                User, 
                                verbose_name = "Пользователь",
                                )
    log_type = models.IntegerField(
                                choices=TYPE_CHOICES, 
                                verbose_name = "Тип события",
                                )
    log_status = models.CharField(
    							max_length=10,
                                verbose_name = "Статус",
                                )
    log_date = models.DateTimeField(
                                default=timezone.now, 
                                verbose_name = "Дата создания",
                                )
    
    def __str__(self):
        return str(self.log_type)
    
    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Лог"
