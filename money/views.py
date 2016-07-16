# -*- coding:utf-8 -*-

from django.shortcuts import render

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from logs.models import Logs
from money.models import Post, Tarif

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

import requests
import lxml.html

from local_site.settings import TYPE_CHOICES
from django.utils import timezone
from datetime import datetime, date, time, timedelta

def run_money_parser(request):
    if request.user.is_superuser:
        money_pay_users = User.objects.filter(is_superuser=False)

    for m_user in money_pay_users:
        money_check(m_user)

    log_list = Logs.objects.filter(log_type=6).order_by('-log_date')[:10]

    for l in log_list:
        l.log_type = TYPE_CHOICES[int(l.log_type)-1][1]

    data = {
        'users_count': User.objects.all().count(),
        'logs_count': Logs.objects.all().count(),
        'log_list': log_list,
    }

    return render(request, 
                'money/run_money_parser.html', 
                data,
                )

def money_check(check_user):
    """
    Нужно чтоб были импортированы:
    UserProfile, User, Post, Logs
    requests, lxml.html
    """
    pr_user = UserProfile.objects.get(user_id=check_user.id)    
    try:
        r = requests.post(
                'http://www.wimagic.com.ua/1.php', 
                # 'http://www.wimagicss.com.ua/1.php', 
                data = {
                    'login':check_user.username, 
                    'pass':pr_user.pwd
                        }
                    )
        html = lxml.html.fromstring(r.text)
        money_r = html.xpath("/html/body/table/tr[1]/td[4]/text()")[0]

        new = Post(money=money_r, user=check_user)
        new.save()
        
        log = Logs(log_user = check_user, log_type = 6, log_status = "Успех",)
        log.save()
    except:
        log = Logs(log_user = check_user, log_type = 6, log_status = "Неудача",)
        log.save()


@login_required(login_url='/user/login/')
def user_check_money(request, pk):
    m_user = get_object_or_404(User, username=pk)
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=m_user).last()


    if timezone.localtime(timezone.now()) - money_last.created_date  > timedelta(minutes=5):
        money_check(m_user)
        money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
        tarif_last = Tarif.objects.filter(user=m_user).last()
        cheker = True
    else:
        state_type = 'warning'
        state_message = 'Принудительно проверять деньги чаще чем раз в пять минут нельзя!'
        cheker = False

    if tarif_last:
        from number_to_text import num2text
        male_units = ((u'день', u'дня', u'дней'), 'm')
        days_left = num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units)
    else:
        days_left = None

    log_list = Logs.objects.filter(log_user=m_user).order_by('-log_date')[:10]

    for l in log_list:
        l.log_type = TYPE_CHOICES[int(l.log_type)-1][1]

    # print(log_list.first().log_status)
    if cheker != False:
        if log_list.first().log_status == "Неудача":
            state_type = 'danger'
            state_message = 'Что-то пошло не так, подробнее в логе...'
        if log_list.first().log_status == "Успех":
            state_type = 'success'
            state_message = 'Все прошло как надо'


    state = {
    'state_type':state_type,
    'state_message':state_message,
    }
    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        'tarif_last':tarif_last,
                                                        'days_left':days_left,
                                                        'log_list': log_list,
                                                        'state':state,
                                                        })

def home(request):
    
    return render(request, 'home.html', {
                                                        # 'm_user': m_user,
                                                        # 'pr_user': pr_user,
                                                        # 'money_last':money_last,
                                                        # 'tarif_last':tarif_last,
                                                        # 'days_left':days_left,
                                                        })