# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Post, Tarif

# Register your models here.

# admin.site.register(Post)
admin.site.register(Tarif)


class PostAdmin(admin.ModelAdmin):
    # в таблице списка постов выводить только колонку title, если вы добавите еще одно имя поля, то и оно выведется
    list_display = ('user', 'money', 'created_date',)

# связываем эту модель с моделью PostAdmin
admin.site.register(Post, PostAdmin)