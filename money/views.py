# -*- coding:utf-8 -*-

from django.shortcuts import render

from django.contrib.auth.models import User
from userprofile.models import UserProfile
from logs.models import Logs
from money.models import Post, Tarif
from news.models import News

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

import requests
import lxml.html

from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from number_to_text import num2text

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
        'LOGSTATUSYES':LOGSTATUSYES,
        'LOGSTATUSNO':LOGSTATUSNO,
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
        
        log = Logs(log_user = check_user, log_type = 6, log_status = LOGSTATUSYES,)
        log.save()
    except:
        log = Logs(log_user = check_user, log_type = 6, log_status = LOGSTATUSNO,)
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
        state_message = '<strong>Внимание!</strong> Принудительно проверять деньги чаще чем раз в пять минут нельзя!'
        cheker = False

    if tarif_last:
        male_units = ((u'день', u'дня', u'дней'), 'm')
        days_left = num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units)
    else:
        days_left = None

    log_list = Logs.objects.filter(log_user=m_user).order_by('-log_date')[:10]

    for l in log_list:
        l.log_type = TYPE_CHOICES[int(l.log_type)-1][1]

    # print(log_list.first().log_status)
    if cheker != False:
        if log_list.first().log_status == LOGSTATUSNO:
            state_type = 'danger'
            state_message = '<strong>Ошибка!</strong> Что-то пошло не так. Попробуйте повторить немножко позже.'
        if log_list.first().log_status == LOGSTATUSYES:
            state_type = 'success'
            state_message = '<strong>Отлично!</strong> Все прошло как надо! Данные обновлены!'


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
                                                        'LOGSTATUSYES':LOGSTATUSYES,
                                                        'LOGSTATUSNO':LOGSTATUSNO,
                                                        })

def home(request):
    users_count = User.objects.filter(is_superuser=False).count()
    male_units = ((u'пользователь', u'пользователя', u'пользователей'), 'm')
    users_count = num2text(users_count, male_units)
    money_count = 0
    tarif_count = 0

    for us in User.objects.filter(is_superuser=False):
        money_count = money_count + Post.objects.filter(user=us).last().money
        tarif = Tarif.objects.filter(user=us).last()
        if tarif != None:
            tarif_count = tarif_count + Tarif.objects.filter(user=us).last().money_for_mons/30
        else:
            tarif_count = tarif_count + 0

    female_units = ((u'гривна', u'гривен', u'гривен'), 'f')
    money_count = num2text(money_count, female_units)
    tarif_count = num2text(tarif_count, female_units)

    data = {
        'users_count': users_count,
        'money_count': money_count,
        'tarif_count': tarif_count,
        'commits':News.objects.filter(news_type=2).order_by('-created_date')[:3],
        'news_wed':News.objects.filter(news_type=1).order_by('-created_date')[:3],
    }
    # e_send_on_50(request)
    return render(request, 'home.html', data,)

from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.mail import send_mail
from local_site.settings import EMAIL_HOST_USER

def e_send_on_email(request):
    subject = 'Wimagic-alert теперь знает Вашу почту!'
    money_last = Post.objects.filter(user=request.user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=request.user).last()
    male_units = ((u'день', u'дня', u'дней'), 'm')

    context = {
        'title': subject, 
        'pr_user': UserProfile.objects.get(user_id=request.user.id),
        'money_last': money_last,
        'days_left': num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units),
        }

    txt = render_to_string('email/on_email.txt', context)
    html = render_to_string('email/on_email.html', context)

    send_mail(subject, txt, EMAIL_HOST_USER, ['kowalew.backup@gmail.com'], 
          fail_silently=False, html_message=html)


def e_send_on_50(request):
    subject = 'У Вас уже меньше 50грн. на балансе.'
    money_last = Post.objects.filter(user=request.user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=request.user).last()
    male_units = ((u'день', u'дня', u'дней'), 'm')
    # (tarif_last.money_for_mons/30)
    context = {
        'title': subject, 
        'pr_user': UserProfile.objects.get(user_id=request.user.id),
        'money_last': money_last,
        'tarif_last':tarif_last.money_for_mons/30,
        'days_left': num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units),
        'request':request,
        }

    txt = render_to_string('email/on_50.txt', context)
    html = render_to_string('email/on_50.html', context)

    send_mail(subject, txt, EMAIL_HOST_USER, ['kowalew.backup@gmail.com'], 
          fail_silently=False, html_message=html)