# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    user = models.ForeignKey(User, unique=True, related_name='profile')
    pwd = models.CharField(max_length=200, verbose_name='PWD')
    middle_name = models.CharField(max_length=200, verbose_name='Отчество')
    vk_link = models.CharField(max_length=200, verbose_name='Учетка на Vk')  
    ok_link = models.CharField(max_length=200, verbose_name='Учетка на Ok')  
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

#Обратиться к добавленному свойству модели можно так:
#u = User.objects.get(username='johny')
#johny_avatar = u.userprofile.avatar
