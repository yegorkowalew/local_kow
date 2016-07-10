# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone

class News(models.Model):
    title = models.CharField(
                        max_length=200,
                        verbose_name = "Название новости",
                        )
    text = models.TextField(
                        verbose_name = "Содержание новости",
                        )
    created_date = models.DateTimeField(
                        default=timezone.now, 
                        verbose_name = "Дата создания",
                        )
    parsed_date = models.DateTimeField(
                        default=timezone.now, 
                        verbose_name = "Дата парсера", 
                        blank=True, 
                        null=True
                        )

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
