# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone
from local_site.settings import NEWS_CHOICES

class News(models.Model):
    title = models.CharField(
                        max_length=200,
                        verbose_name = "Название новости",
                        )
    text = models.TextField(
                        verbose_name = "Содержание новости",
                        blank = True,
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
    news_type = models.IntegerField(
                        choices=NEWS_CHOICES, 
                        verbose_name = "Тип новости",
                        )
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
