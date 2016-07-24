# -*- coding:utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm, PreferencesUserForm, LoginUserForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from money.models import Post, Tarif

from logs.models import Logs

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from local_site.settings import TYPE_CHOICES, LOGSTATUSYES, LOGSTATUSNO

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['user_login'], password=request.POST['user_pass'])
            login(request, user)
            return HttpResponseRedirect('/user/'+request.user.username)
    else:
        form = RegisterUserForm()
    return render(request, 'userprofile/register_user.html', {'form': form})

@login_required(login_url='/user/login/')
def user_detail(request, pk):
    m_user = get_object_or_404(User, username=pk)
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=m_user).last()

    if tarif_last:
        from number_to_text import num2text
        male_units = ((u'день', u'дня', u'дней'), 'm')
        days_left = num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units)
    else:
        days_left = None

    log_list = Logs.objects.filter(log_user=m_user).order_by('-log_date')[:10]

    for l in log_list:
        l.log_type = TYPE_CHOICES[int(l.log_type)-1][1]
    state= None
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

@login_required(login_url='/user/login/')
def user_preferences(request, pk):
    m_user = get_object_or_404(User, username=pk)
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=m_user).last()

    if tarif_last:
        from number_to_text import num2text
        male_units = ((u'день', u'дня', u'дней'), 'm')
        days_left = num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units)
        user_tarif = tarif_last
    else:
        days_left = None
        user_tarif = ''

    data = {
        'user_tarif': user_tarif,
        'user_email': m_user.email,
        'user_vk': pr_user.vk_link,
        'user_ok': pr_user.ok_link,        
    }

    if request.method == 'POST':
        form = PreferencesUserForm(request.POST)
        if form.is_valid():
            try:
                obj = Tarif.objects.get(user=m_user)
                obj.money_for_mons = form.cleaned_data['user_tarif']
                obj.save()
            except Tarif.DoesNotExist:
                obj = Tarif(user = m_user, money_for_mons = form.cleaned_data['user_tarif'])
                obj.save()

            m_user.email = form.cleaned_data['user_email']
            m_user.save()
            pr_user.vk_link = form.cleaned_data['user_vk']
            pr_user.ok_link = form.cleaned_data['user_ok']
            pr_user.save()

            return HttpResponseRedirect('/user/'+request.user.username)
    else:
        form = PreferencesUserForm(data, initial=data)


    return render(request, 'userprofile/preferences_user.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        'tarif_last':tarif_last,
                                                        'days_left':days_left,
                                                        'form': form,
                                                        })

def user_login(request):
    if request.user is not None:
        logout(request)
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                                password=form.cleaned_data['user_pass']
                            )
            if user is not None:
                login(request, user)
                log = Logs(log_user = user, log_type = 3, log_status = LOGSTATUSYES,)
                log.save()
                return HttpResponseRedirect('/user/'+request.user.username+'/')
            else:
                data = {
                        'user_name': form.cleaned_data['user_name'],
                        'user_pass': form.cleaned_data['user_pass'],
                        }
                form = LoginUserForm(initial=data)
    else:
        form = LoginUserForm()
    return render(request, 'userprofile/user_login.html', {'form': form,})

def user_logout(request):
    if request.user is not None:
        log = Logs(log_user = request.user, log_type = 5, log_status = LOGSTATUSYES,)
        log.save()
        logout(request)
    return HttpResponseRedirect('/')

def user_admin(request):
    if request.user.is_superuser:
        users = User.objects.all()
        log_list = Logs.objects.order_by('-log_date')[:30]

        # log_list = Logs.objects.filter(log_type=6).order_by('-log_date')[:10]

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
                    'userprofile/user_admin.html', 
                    data,
                    )
    else:
        return HttpResponseRedirect('/')

