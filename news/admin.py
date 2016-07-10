# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import News

# admin.site.register(News)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(News, NewsAdmin)