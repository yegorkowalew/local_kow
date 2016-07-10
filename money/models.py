# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    money = models.FloatField(verbose_name = "Денег на счету",)
    created_date = models.DateTimeField(default=timezone.now, verbose_name = "Дата-время проверки",)
    user = models.ForeignKey(User, verbose_name = "Пользователь")

    def __str__(self):
        return str(self.created_date)
    
    class Meta:
        verbose_name = "Деньги"
        verbose_name_plural = "Деньги"

class Tarif(models.Model):
    money_for_mons = models.PositiveIntegerField(default=200)
    user = models.ForeignKey(User, verbose_name = "Денег на счету")

    def __str__(self):
        return str(self.money_for_mons)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

