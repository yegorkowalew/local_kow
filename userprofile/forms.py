# -*- coding:utf-8 -*-
from django import forms

import requests
import lxml.html

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from money.models import Post

# from django.contrib.auth import authenticate, login

class RegisterUserForm(forms.Form):
    user_login = forms.CharField(
        label='Номер вашего личного счета на сайте wimagic.com.ua', 
        max_length=20, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'type':'text', 
            'placeholder':'Например: 0041703345'}
            )
    )
    user_pass = forms.CharField(
        label='Пароль для входа в личный кабинет',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'type':'password', 
            'placeholder':'Пароль'}
            )
    )
    
    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        user_login = cleaned_data.get("user_login")
        user_pass = cleaned_data.get("user_pass")
        try:
            p = User.objects.get(username=user_login)
        except User.DoesNotExist:
            print ('нужно попытаться завести нового')
            #forms.ValidationError('Пользователь уже есть в базе, нужно попытаться завести нового')
            r = requests.post('http://www.wimagic.com.ua/1.php', data = {'login':user_login, 'pass':user_pass})
            html = lxml.html.fromstring(r.text)
            try:
                rr = html.xpath("/html/body/pre/text()")[0]
                
                raise forms.ValidationError('Сайт провайдера ответил: "' + rr.encode('raw-unicode-escape').decode('utf-8') + '". Вы ввели не правильный номер личного счета, либо не правильный пароль.')
            except IndexError:
                print ('Логин правильный')
                try:
                    money_r = html.xpath("/html/body/table/tr[1]/td[4]/text()")[0] # на счету
                    # print (rr.encode('raw-unicode-escape').decode('utf-8'))
                    rr = html.xpath("/html/body/pre/h2/span[1]")[0]
                    # print (rr.text)
                    rr = html.xpath("/html/body/pre/h2/span[2]")[0] # на счету
                    # print (rr.text.encode('raw-unicode-escape').decode('utf-8'))
                    fio = rr.text.encode('raw-unicode-escape').decode('utf-8').split(' ')
                    
                    # Регистрируем пользователя в системе
                    user = User.objects.create_user(
                                    username = user_login, 
                                    #email = 'lennon@thebeatles.com', 
                                    password = user_pass,
                                    first_name = fio[1],
                                    last_name = fio[0],
                                    )
                    user.save()
                    new = Post(money=money_r, user=user)
                    new.save()
                    try:
                        pr = UserProfile.objects.get(m_user.id)
                    except:
                        # print('нету')
                        user = UserProfile.objects.create(
                                            user_id = user.id,
                                            middle_name = fio[2],
                                            pwd = user_pass
                        )

                    # user = authenticate(username=user_login, password=user_pass)
                    # login(request, user)

                except IndexError:
                    print ('Не правильный номер личного счета или пароль')
                    raise forms.ValidationError('Не правильный номер личного счета или пароль')
            
        else:
            print ('Пользователь уже есть в базе, нужно попытаться авторизировать его')
            raise forms.ValidationError('Пользователь уже есть в базе, нужно попытаться авторизировать его')
    

