# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm, PreferencesUserForm, LoginUserForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from money.models import Post, Tarif

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

    
def pr(request):
    m_user = get_object_or_404(User, username='0041703721')
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    # new = Post(money=100, user=m_user)
    # new.save()

    user = authenticate(username='0041703721', password='kisses85')
    login(request, user)


    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=m_user).last()
    # print(tarif_last)
    if tarif_last:
        from number_to_text import num2text
        male_units = ((u'день', u'дня', u'дней'), 'm')
        days_left = num2text(round(money_last.money/(tarif_last.money_for_mons/30)), male_units)
    else:
        days_left = None
    
    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        'tarif_last':tarif_last,
                                                        'days_left':days_left,
                                                        })

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

    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        'tarif_last':tarif_last,
                                                        'days_left':days_left,
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
        form = PreferencesUserForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            try:
                obj = Tarif.objects.get(user=m_user)
                print(obj.money_for_mons)
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
                return HttpResponseRedirect('/user/'+request.user.username)
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
        logout(request)
    return HttpResponseRedirect('/')