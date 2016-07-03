# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=200, verbose_name='PWD')
 
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

#Обратиться к добавленному свойству модели можно так:
#u = User.objects.get(username='johny')
#johny_avatar = u.userprofile.avatar
