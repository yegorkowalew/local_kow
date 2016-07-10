# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import Logs

# admin.site.register(Logs)


class LogsAdmin(admin.ModelAdmin):
    list_display = ('log_user', 'log_type', 'log_status', 'log_date',)

admin.site.register(Logs, LogsAdmin)